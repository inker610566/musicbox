說明
=====
[HTML5 Music Player (本地拖曳撥放)](http://morris821028.github.io/2014/04/26/html5-music-and-drag-file/)

代碼起源
=====
[tommy351](http://zespia.tw/blog/2012/02/04/lab-html5-audio/) 提供的。基於 HTML5 和 JQuery 運行的撥放器，HTML5 支持 .mp3, .wav, .ogg 這三個種音樂格式的撥放。

HTML5 `<audio>` 支持音樂撥放，撥放種類有限，而且 HTML5 不知道穩定了沒。

* 本次挑戰的項目
	* 增加 ** 拖曳檔案 ** 的撥放
	* 拖曳檔案 和 拖曳資料夾 的摸索
	* HTML5 圍觀

修改
=====

![demo](/img/html5-drag-and-music.PNG)
如上圖，最後一個檔案 `mo - 45. not yet.mp3` 是拖曳上傳的內容。

## 歷程 ## 

* 增加本地拖曳撥放，操作方式為將本地 mp3 檔案上傳

檔案能知道的資訊有限
* `name` 取得檔案名稱，如果需要做副檔名檢查，可利用它。
* `size` 取得檔案大小 (bytes)。
* `type` 取得檔案的 MIME 型別 (若無法對應會傳回空白)。

因為安全性，所以得不到路徑資訊，也就是不能隨便去掃描別人的本地資料。因此要完成資料夾下的所有檔案獲取會有困難。

其實瀏覽器本上就會支持檔案拖曳，並且在新分頁上顯示資訊，如果要避免瀏覽器自己開啟檔案，則使用 `evt.stopPropagation()` 將 drag 相關事件關閉，也就是說在當前頁面的 drag 事件都不會被瀏覽器知曉。

## 後記 ##
* 對於 `.mp3` 檔案要自動獲得專輯封面可能嗎？
	請參考 [這裡](http://stackoverflow.com/questions/1645803/how-to-read-mp3-file-tags)
```
 Field      Length    Offsets
 Tag        3           0-2
 Songname   30          3-32
 Artist     30         33-62
 Album      30         63-92
 Year       4          93-96
 Comment    30         97-126
 Genre      1           127
```
	要自己擠去 parsing 這些資訊還是算了吧。WRYYYYY

* 對於資料夾整包拖曳操作？HTML5 drag upload folder
	在寫這篇的時候，網路上有 [demo](http://html5-demos.appspot.com/static/dnd/all_types_of_import.html)，但是只有在 chrome 21 下才有支持，看起來是從瀏覽器 ( 本地軟件 ) 來協助遍歷資料夾下的內容。不然是沒有權限去運行的。

* 讀取的異步操作 ?
	是的，最近在編寫時常會遇到異步操作，也就是必須全用 `callback` 來完成，因為讀檔的資訊完成的 `callback function` 中並沒有 `file.name` 之類的資訊，如果適用 `for(var i in files)` 運行，會發生變數找不到的情況，因此用 `$.each()` 和 `reader.onload()` 來完成這個操作。

	* onloadstart、onprogress、onload、onabort、onerror 和 onloadend 這幾個可以協助監控上傳資訊，也就是能知曉現在上傳進度 ... 等。
