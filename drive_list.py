from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os, io
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

"""files = DRIVE.files().list().execute().get('files', [])
for f in files:
    print(f['name'], f['mimeType'])"""

def downloadFile(file_id,filepath):
    request = DRIVE.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())
def searchFile(query):
    results = DRIVE.files().list(fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    """if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))"""
    return items
#uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
#downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')
#createFolder('Google')
"""items=searchFile("'1moBoJF5VGtoY5Wf-dj8EXAON8QiLseQh' in parents")
for item in items:
    downloadFile(item['id'],'./gdownload/%s'%(item['name']))"""


def retaining_folder_structure(query,filepath):
	results = DRIVE.files().list(fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
	items = results.get('files', [])
	for item in items:
		print(item['name'])
		if item['mimeType']=='application/vnd.google-apps.folder':
			fold=item['name']
			path=filepath+'/'+fold
			if os.path.isdir(path):
				retaining_folder_structure("'%s' in parents"%(item['id']),path)
			else:
				os.mkdir(path)
				retaining_folder_structure("'%s' in parents"%(item['id']),path)
		else:
			request = DRIVE.files().get_media(fileId=item['id'])
			fh = io.BytesIO()
			downloader = MediaIoBaseDownload(fh, request)
			done = False
			while done is False:
				status, done = downloader.next_chunk()
				print("Download %d%%." % int(status.progress() * 100))
			path=filepath+'/'+item['name']
			#print(path)
			with io.open(path,'wb') as f:
				fh.seek(0)
				f.write(fh.read())

retaining_folder_structure("'1moBoJF5VGtoY5Wf-dj8EXAON8QiLseQh' in parents",'/home/dhanush/experiment')
    



