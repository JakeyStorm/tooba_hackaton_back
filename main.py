from flask import Flask, request, jsonify
import pandas as pd
from recommendations import get_user_recommendations, load_data

app = Flask(__name__)

payments, campaigns, small_user_campaign_matrix, user_similarity_df_small = load_data()

@app.route('/recommendations', methods=['GET'])
def recommendations():
    user_id = request.args.get('user_id')

    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400

    recommendations = get_user_recommendations(user_id, small_user_campaign_matrix, user_similarity_df_small, top_n=3)

    if not recommendations:
        return jsonify({"message": "No recommendations found for this user"}), 404

    recommended_campaigns_info = campaigns[campaigns['id'].isin(recommendations)]

    recommended_campaigns_info['recommended_amount'] = payments[payments['campaign_id'].isin(recommendations)][
        'amount'].mean()

    response = recommended_campaigns_info[['id', 'title', 'description', 'recommended_amount']].to_dict(
        orient='records')

    return jsonify(response)
#
if __name__ == '__main__':
    app.run(debug=True)
