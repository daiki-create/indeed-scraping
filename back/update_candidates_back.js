

function update_csv(){

  //応募者管理シートをcsvに出力・・・csv1
  var sheetName='sheet1';

  var ss=SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(sheetName);

  var first_row=13
  var last_row=sheet.getLastRow();
  var values1 = sheet.getRange(first_row,2,last_row,9).getValues();  
  Logger.log(values1);

  var csv1=values1.join('\n');
  Logger.log(csv1)

  var blob = Utilities.newBlob(csv1, MimeType.CSV, sheetName + '.csv');
  var candidates = '1mnQhUyP0cvRwcFWlNAWml6EsKfcr8Qgb'; 
  var folder = DriveApp.getFolderById(candidates);
  //folder.createFile(blob);

  //応募者管理シートから出力したcsvの行数を取得・・・row1
  var row1=values1.length;
  Logger.log(row1);

  //pythonで作成したcsv(重複削除済み)をCドライブから読み込む・・・csv2
  //二次元配列化・・・values2
  var values2=import_csv();
  Logger.log('import csv')
  Logger.log(values2);
  Logger.log('二次元配列2')


  //values2の列数を8にする
  var array=['a','b','c','d','e'];
  for(i=0;i<values2.length;i++){
    Logger.log(values2[i])
    if(i%2==0){
      values2[i].push('','','','','',values2[i][2])
      values2[i][2]=''
      Logger.log(values2[i])
    }
    else{
      delete values2[i];
    }
  }
  Logger.log(values2)
  Logger.log('3から9にした二次元配列2')

  //values2の1列目とvalues1の1列目で重複のある要素を削除・・・values3
  //values2とvalues1を結合・・・values12
  var values12=values1.concat(values2)
  Logger.log(values12)
  Logger.log('結合')

  //重複のある要素を削除
  const values3 = values12.filter(function(e, index){
    return !values12.some(function(e2, index2){
      return index > index2 && e[0] == e2[0];
    });
  });
  Logger.log(values3)
  Logger.log('重複削除')

  //values3の行数を取得・・・row3
  var row3=values3.length;
  Logger.log(row3);
  Logger.log('二次元配列3')

  //values3をcsvにする・・・csv3
  var csv3=values3.join('\n');
  Logger.log(csv3);
  Logger.log('csv3')

  //values3をスプレッドに追加
  sheet.getRange(first_row,2,row3,9).setValues(values3);
  Logger.log('ok');
}


function import_csv(){

  //csvファイルの読み込み
  var new_candidates_key='1XPdgzlRgr9mlCod6LrSf9ij4Mrh_Sr19';
  const files = DriveApp.getFolderById(new_candidates_key).getFiles();
  while (files.hasNext()) {
    const file = files.next();
    const filename = file.getName();
    Logger.log(filename)
    var csv2 = file.getBlob().getDataAsString("Shift_JIS");
    Logger.log(csv2)
  }

  
  //csvを二次元配列化
  var values2=Utilities.parseCsv(csv2);

  return values2;
}