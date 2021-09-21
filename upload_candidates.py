from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# 認証を行う --- (*2)
gauth = GoogleAuth()
gauth.CommandLineAuth()
print("ok")

drive = GoogleDrive(gauth)

file_metadata = {
    'title': "roo.csv",
    'minetype':"text/csv",
    'parents': [{
    'id': '1XPdgzlRgr9mlCod6LrSf9ij4Mrh_Sr19',
    'kind': 'drive#fileLink',
}],
}
print("ok")

f = drive.CreateFile(file_metadata)
print("ok")

f.SetContentFile('candidates.csv')
print("ok")

f.Upload()
print("ok")

#フォルダキー
#1XPdgzlRgr9mlCod6LrSf9ij4Mrh_Sr19