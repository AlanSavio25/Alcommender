import requests

url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

querystring = {"returnFaceId":"true","returnFaceLandmarks":"false","returnFaceAttributes":"emotion,age,gender"}

image_path = "/home/apurv/Pictures/googleVision.png"
image_data = open(image_path, "rb").read()

#payload = "{\n    url : \"https://scontent-lht6-1.xx.fbcdn.net/v/t1.15752-9/47304443_334903183958909_5131817084937830400_n.jpg?_nc_cat=108&_nc_ht=scontent-lht6-1.xx&oh=6b3bf1fc840c14904edf5555f292b9e6&oe=5CB18F3E\"\n}"

headers = {
    'Ocp-Apim-Subscription-Key': "9495f13ff2764d0f87daec1d820257e8",
    'Content-Type': "application/octet-stream",
    'cache-control': "no-cache",
    'Postman-Token': "67ac9f11-e73a-430f-aca3-eb71b7dcc0a5"
    }

response = requests.request("POST", url, data=image_data, headers=headers, params=querystring)

print(response.text)