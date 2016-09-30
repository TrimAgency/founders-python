from flask import Flask
from flask import request, Response
import json
from facebookads.api import FacebookAdsApi
from facebookads import objects
import os
app = Flask(__name__, static_url_path='')

os.environ['PORT']
USER_ID="520339341493154"
USER_SECRET="bef97c0f80599becdccd966e4dd0ab5f"
USER_TOKEN="EAAHZAPvGcw6IBAMxqXkC3a5BWWXKD3Kt2Mp6nSREMza3wI9ZCmMiKYDnzCefKOb8lTNdmIFOg6KtJhPZB3yIwSuEA64rBSZCcEBSBgvpwTEitaHUJM461nw8F0EGhuZAxUBv3TWMmCZCZCQfFZBtYzEqLVbYBMbLIIOOA2O9n1RLXgZDZD"

FacebookAdsApi.init(USER_ID, USER_SECRET, USER_TOKEN)
me = objects.AdUser(fbid='me')
account = me.get_ad_account()

fields = [
    objects.Insights.Field.clicks,
    objects.Insights.Field.cpc,
    objects.Insights.Field.spend,
    objects.Insights.Field.campaign_id,
    objects.Insights.Field.campaign_name,
    objects.Insights.Field.ad_id,
    objects.Insights.Field.ad_name,
    objects.Insights.Field.adset_name,
    objects.Insights.Field.adset_id
    ]

def get_keys(object):
  insight = {}
  for field in fields:
    insight[field] = object[field]
  return insight

def get_insights():
  params = { 'level' : objects.Insights.Level.ad }
  insights = account.get_insights(params=params, fields=fields)
  return [get_keys(insight) for insight in insights]

@app.route("/insights", methods=['GET'])
def insights():
  insights = get_insights()
  res = json.dumps(insights)
  return Response(res, mimetype='application/json')

@app.errorhandler(404)
def page_not_found(e):
  return app.send_static_file('index.html')


if __name__ == "__main__":
  app.run(
      port=os.environ['PORT']
      )
