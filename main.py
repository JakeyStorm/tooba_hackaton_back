# from flask import Flask, request, jsonify
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
# import scipy.sparse as sp
#
# app = Flask(__name__)
#
# # Загрузка данных с листа 'Query result' для платежей и кампаний
# payments = pd.read_excel('payments.xlsx', sheet_name='Query result')
# campaigns = pd.read_excel('campaigns.xlsx', sheet_name='Query result')
#
# # Создание матрицы пользователь-сбор (User-Item Matrix)
# small_user_campaign_matrix = payments.pivot_table(index='user_id', columns='campaign_id', values='amount', fill_value=0).iloc[:100, :]
#
# # Преобразование в разреженную матрицу для экономии памяти
# small_user_campaign_matrix_sparse = sp.csr_matrix(small_user_campaign_matrix.values)
#
# # Вычисление косинусного сходства между пользователями
# user_similarity_small = cosine_similarity(small_user_campaign_matrix_sparse)
# user_similarity_df_small = pd.DataFrame(user_similarity_small, index=small_user_campaign_matrix.index, columns=small_user_campaign_matrix.index)
#
# def get_user_recommendations(user_id, user_campaign_matrix, user_similarity_df, top_n=5):
#     similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:]
#     similar_users_campaigns = user_campaign_matrix.loc[similar_users].sum(axis=0)
#     user_campaigns = user_campaign_matrix.loc[user_id]
#     recommendations = similar_users_campaigns[user_campaigns == 0].sort_values(ascending=False)
#     return recommendations.head(top_n).index.tolist()
#
# @app.route('/recommendations', methods=['GET'])
# def recommendations():
#     user_id = request.args.get('user_id')
#
#     if user_id is None:
#         return jsonify({"error": "User ID is required"}), 400
#
#     if int(user_id) not in small_user_campaign_matrix.index:
#         return jsonify({"error": "User ID not found"}), 404
#
#     recommendations = get_user_recommendations(int(user_id), small_user_campaign_matrix, user_similarity_df_small, top_n=3)
#
#     if not recommendations:
#         return jsonify({"message": "No recommendations found for this user"}), 404
#
#     recommended_campaigns_info = campaigns[campaigns['id'].isin(recommendations)]
#     recommended_campaigns_info['recommended_amount'] = payments[payments['campaign_id'].isin(recommendations)]['amount'].mean()
#
#     response = recommended_campaigns_info[['id', 'title', 'description', 'recommended_amount']].to_dict(orient='records')
#
#     return jsonify(response)
#
# if __name__ == '__main__':
#     app.run(debug=True)
