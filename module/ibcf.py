#membuat fungsi untuk menampilkan 10 top movie dengan nilai similarity tertinggi
def top_movies(movies_title):
    count = 1
    print('movie yang sama dengan {} include:\n'.format(movies_title))
    for item in item_sim_dataset.sort_values(by = movies_title, ascending = False).index[1:11]:
        print('No. {}: {}'.format(count, item))
        count +=1
        
#membuat fungsi utk menampilkan top 5 user dengan nilai similarity tertinggi
def top_users(user):
    
    if user not in matriks_norm.columns:
        return('tdak ada data tersedia di user {}'.format(user))
    
    print('user paling mirip:\n')
    sim_values = user_sim_dataset.sort_values(by=user, ascending=False).loc[:,user].tolist()[1:11]
    sim_users = user_sim_dataset.sort_values(by=user, ascending=False).index[1:11]
    zipped = zip(sim_users, sim_values,)
    for user, sim in zipped:
        print('User #{0}, nilai similarity: {1:.2f}'.format(user, sim))
        
#membuat fungsi daftar yg berisi movie dengan nilai similarity tertinggi per pengguna yang mirip/serupa
#dan mengembalikan nama movie yang memliki nilai similarity yg sama pda daftar
def similar_user_recs(user):
    
    if user not in matriks_norm.columns:
        return('tdak ada data tersedia di user {}'.format(user))
    
    sim_users = user_sim_dataset.sort_values(by=user, ascending=False).index[1:11]
    best = []
    most_common = {}
    
    for i in sim_users:
        max_score = matriks_norm.loc[:, i].max()
        best.append(matriks_norm[matriks_norm.loc[:, i]==max_score].index.tolist())
    for i in range(len(best)):
        for j in best[i]:
            if j in most_common:
                most_common[j] += 1
            else:
                most_common[j] = 1
    sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_list[:5]

#membuat fungsi rata-rata prediksi dari user yang serupa
#untuk menentukan rating yng bgus utk user
def predicted_rating(movies_title, user):
    sim_users = user_sim_dataset.sort_values(by=user, ascending=False).index[1:668]
    user_values = user_sim_dataset.sort_values(by=user, ascending=False).loc[:,user].tolist()[1:668]
    rating_list = []
    weight_list = []
    for j, i in enumerate(sim_users):
        rating = matriks.loc[i, movies_title]
        similarity = user_values[j]
        if np.isnan(rating):
            continue
        elif not np.isnan(rating):
            rating_list.append(rating*similarity)
            weight_list.append(similarity)
    try:
        result = sum(rating_list)/sum(weight_list)
    except ZeroDivisionError:
        result = 0
    return result