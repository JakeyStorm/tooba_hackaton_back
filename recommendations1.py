import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp


def load_data(payments_path='payments.csv', campaigns_path='campaigns.csv'):
    payments = pd.read_csv(payments_path)
    campaigns = pd.read_csv(campaigns_path)

    payments['amount'] = pd.to_numeric(payments['amount'], errors='coerce')
    payments['amount'] = payments['amount'].fillna(0)

    small_user_campaign_matrix = payments.pivot_table(index='user_id', columns='campaign_id', values='amount',
                                                      fill_value=0)

    small_user_campaign_matrix_sparse = sp.csr_matrix(small_user_campaign_matrix.values)

    user_similarity_small = cosine_similarity(small_user_campaign_matrix_sparse, dense_output=False)
    user_similarity_df_small = pd.DataFrame(user_similarity_small.toarray(), index=small_user_campaign_matrix.index,
                                            columns=small_user_campaign_matrix.index)

    return payments, campaigns, small_user_campaign_matrix, user_similarity_df_small


def get_user_recommendations(user_id, user_campaign_matrix, user_similarity_df, top_n=5):
    if user_id not in user_similarity_df.index:
        return []

    similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:]

    similar_users_campaigns = user_campaign_matrix.loc[similar_users].sum(axis=0)

    user_campaigns = user_campaign_matrix.loc[user_id]
    recommendations = similar_users_campaigns[user_campaigns == 0].sort_values(ascending=False)

    return recommendations.head(top_n).index.tolist()
