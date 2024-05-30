"""
This script upload an pdf file to take the sourceId
Then, using the sourceId, it asks multiple questions to the pdf file
This means the asking_question function can be called multiple times until user_input is 'exit'
"""
import requests
import argparse

def upload_pdf(file_path, api_key):
    files = [
        ('file', ('file', open(file_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': api_key
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        return response.json()['sourceId']
    else:
        return None
    
def asking_question(source_id, question, api_key):
    headers = {
    'x-api-key': api_key,
    "Content-Type": "application/json",
}

    data = {
        'sourceId': source_id,
        'messages': [
            {
                'role': "user",
                'content': question,
            }
        ]
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    if response.status_code == 200:
        print('Result:', response.json()['content'])
        # append the question and the response to a file name source_id.txt
        with open(f'{source_id}.txt', 'a') as f:
            f.write(f'Question: {question}\n')
            f.write(f'Response: {response.json()["content"]}\n\n')
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)

def main():
    api_key = 'sec_o4URyzbHWX2GX9kX89d1ObzvHD4dnXyh'
    parser = argparse.ArgumentParser(description='Ask questions to a pdf file and save the responses to a file. If not the -f but the -s is provided, the script will ask the questions to the sourceId provided.')
    parser.add_argument('-f', '--file', type=str, help='Path to the pdf file')
    parser.add_argument('-s', '--sourceId', type=str, help='SourceId of the pdf file')
    args = parser.parse_args()
    if args.sourceId:
        source_id = args.sourceId
    else:
        source_id = upload_pdf(args.file, api_key)
    if source_id is None:
        print('Error uploading the file or invalid sourceId. Please try again.')
        return
    else :
        print('File uploaded successfully or sourceId provided. You can start asking questions. Type "exit" to finish the script.')
        print('SourceId:', source_id)
        question = ''
        while question != 'exit':
            question = input('Enter your question: ')
            if question != 'exit':
                asking_question(source_id, question, api_key)
            else:
                print('Thank you for using the script')
                return
            
if __name__ == '__main__':
    main()


