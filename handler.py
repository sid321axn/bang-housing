import json
from sklearn.externals import joblib
import pickle

gboost_pkl_filename = 'gboost_classifier_20190929.pkl'
gboost_model_pkl = open(gboost_pkl_filename,'rb')
model = pickle.load(gboost_model_pkl)

#model = joblib.load(model_name)

def predict(event, context):
    body = {
        "message": "Ok",
    }

    params = event['queryStringParameters']
    
    area_type  = int(params['area_type'])
    availability = float(params['availability'])
    balcony = float(params['balcony'])
    bath = int(params['bath'])
    pincode = int(params['pincode'])
    total_sqft = float(params['total_sqft'])
    size_BHK = int(params['size_BHK'])
    size_bed = int(params['size_bed'])

    inputVector = [total_sqft, pincode, area_type, availability, balcony, size_BHK, bath, size_bed]
    data =[inputVector]
    predictedPrice = model.predict(data)[0]
    predictedPrice = round(predictedPrice,2)
    body['predictedPrice'] = predictedPrice
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin": "*"   
        }
    }

    return response

def do_main():
    event = {
        'queryStringParameters': {
            'area_type': 1,
            'availability': 1,
            'balcony': 2,
            'bath': 4,
            'pincode': 560100,
            'total_sqft': 1200,
            'size_BHK': 2,
            'size_bed': 0


                                 }
            }
       
    response = predict(event,None)
    body = json.loads(response['body'])
    print('Price:', body['predictedPrice'])

    with open('event.json', 'w') as event_file:
        event_file.write(json.dumps(event))


do_main()

    


