# -*- coding: utf-8 -*-
from dataapi import Client
if __name__ == "__main__":
    try:
        client = Client()
        client.init('c5a5065318ff2e67a18ae6da29d6e10b22f2b7dc8d65d00e626fbb7de99feed0')
        url1='/api/macro/getChinaDataGDP.csv?field=&indicID=M010000002&indicName=&beginDate=&endDate='
        code, result = client.getData(url1)
        if code==200:
            print(result)
        else:
            print (code)
            print (result)
        url2='/api/subject/getThemesContent.csv?field=&themeID=&themeName=&isMain=1&themeSource='
        code, result = client.getData(url2)
        if(code==200):
            file_object = open('thefile.csv', 'w')
            file_object.write(result.decode())
            file_object.close( )
        else:
            print (code)
            print (result)
    except Exception as e:
        #traceback.print_exc()
        raise e
