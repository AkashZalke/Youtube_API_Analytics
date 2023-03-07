import os
import csv 
import ast
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_main(api_key,region_code,categories,subs_greater_than,subs_lesser_than):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    string_category = ""
    for category in categories:
        string_category+=(category+',')
        
    request = youtube.search().list(
        part="snippet",
        channelType="any",
        maxResults=50,
        q=string_category,
        regionCode=region_code
    )
    response = request.execute()

    # x = ast.literal_eval(response)
    
    channel_Ids_list = set()
    for res in response['items']:
        channel_Ids_list.add(res['snippet']['channelId'])
    print(channel_Ids_list)

    channel_greater_than_number= []

    for channel in channel_Ids_list:
        cur_id = channel
        request_channel = youtube.channels().list(
            part="snippet,statistics",
            id=cur_id
        )

        response_channel = request_channel.execute()
        try:
            channel_name =  response_channel['items'][0]['snippet']['title']
            sub_count  =  response_channel['items'][0]['statistics']['subscriberCount']
            view_count =  response_channel['items'][0]['statistics']['viewCount']
            video_count = response_channel['items'][0]['statistics']['videoCount']
        except:
            continue


        if int(sub_count) > subs_greater_than:
            channel_link = 'https://www.youtube.com/channel/'+cur_id
            temp_dict = {
                'channel_name':channel_name,
                'channel_link':channel_link,
                'sub_count':int(sub_count),
                'view_count':int(view_count),
                'video_count':int(video_count),
                'region':region_code,
            }
            channel_greater_than_number.append(temp_dict)

    fields = ['channel_name','channel_link','sub_count', 'view_count','video_count','region'] 
    with open('channels_info.csv', 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writeheader() 
        writer.writerows(channel_greater_than_number)

if __name__ == "__main__":
    categories = ['Film and Animation2','Autos and Vehicles3' ,'Music','Pets & Animals','Sports','Travel and Events'
                  'Gaming','People and Blogs','Comedy','Entertainment','News and Politics','How-to and Style13',
                  'Education','Science and Technology','Nonprofits and Activism']
    
    api_key = "AIzaSyB6blaudNanXtMoX3OEnUL-mogQxBUCmjw"
    region_code = 'US'
    subs_greater_than = 80000
    subs_lesser_than = float('inf')

    get_main(api_key,region_code,categories,subs_greater_than,subs_lesser_than)
