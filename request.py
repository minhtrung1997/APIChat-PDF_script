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
        # print the error message
        print('Status:', response.status_code)
        print('Error:', response.text)
        return None
    
def upload_link(link, api_key):
    headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
    }
    data = {'url': link}

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-url', headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['sourceId']
    else:
        # print the error message
        print('Status:', response.status_code)
        print('Error:', response.text)
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
    parser.add_argument('-l', '--link', type=str, help='Link to the pdf file')
    args = parser.parse_args()
    # Exit if no file or sourceId or link is provided
    if args.file is None and args.sourceId is None and args.link is None:
        print('Please provide a file or sourceId or link')
        return
    if args.sourceId:
        source_id = args.sourceId
    elif args.link:
        source_id = upload_link(args.link, api_key)
    elif args.file:
        source_id = upload_pdf(args.file, api_key)
    if source_id is None:
        print('Error uploading the file/link or invalid sourceId. Please try again.')
        return
    else :
        print('File/link uploaded successfully or sourceId provided. You can start asking questions. Type "exit" to finish the script.')
        print('SourceId:', source_id)
        question = ''
        while True:
    # Input the question from the user, fix the surplus enter \n
            question = input('Enter your question: ').strip()
            while not question:
                print("You didn't enter a question. Please try again.")
                question = input('Enter your question: ').strip()
            if question == 'exit':
                print('Thank you for using the script')
                return
            else:
                asking_question(source_id, question, api_key)
            
if __name__ == '__main__':
    main()


