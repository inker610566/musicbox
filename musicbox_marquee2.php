<html>

<head>
<meta charset="UTF-8">
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">

<style>
#progress_bar {
	margin: 20px;
	width: 200px;
	height: 4px;
	overflow: hidden;
	cursor: pointer;
}

#played_progress {
	z-index: 2;
	width: 0%;
	height: 4px;
	cursor: pointer;
}

#buffered_progress {
	z-index: 1;
	width: 60px;
	height: 4px;
	cursor: pointer;
}

.control-button{
	margin: 10px;
	float: left;
}

#playlist{
	margin: 10px;
	width: 300px;
	overflow: hidden;
	clear: left;
}


.playitem{
	width: 300px;
	height: 30px;
	white-space: nowrap;
	padding: 5px;
}

.playable{
	cursor: pointer;
}

.moving{
	position: absolute;
}

.playitem-separator{
	height: 1px;
	width: 300px;
	border-radius: 1px;
}

#volume_bar{
	float: left;
	margin: 8px;
	cursor: pointer;
}

.vbar{
	width: 5px;
	float: left;
	margin: 2px;
}

#style-panel{
	position: absolute;
	left: 350px;
	top: 20px;
}

.placer-active{
	background: gold;
}

</style>

<link rel="stylesheet" type="text/css" href="css/day.css" />

</head>
<body id="bdy">

<div id="style-panel">
	<div id="star" class="btn btn-default glyphicon glyphicon-star"> </div>
</div>

<audio id="player" src="music/%E3%80%90GUMI%E3%80%91%E8%A2%AB%E5%AE%B3%E5%A6%84%E6%83%B3%E6%90%BA%E5%B8%AF%E5%A5%B3%E5%AD%90%EF%BC%88%E7%AC%91%EF%BC%89%E3%80%90%E3%82%AA%E3%83%AA%E3%82%B8%E3%83%8A%E3%83%AB%E3%80%91.mp3">
FireFox GG!!<br>
Try to use chrome?<br>
</audio>


<div id="progress_bar">
	<div id="played_progress"> </div>
	<div id="buffered_progress"> </div>
</div>

<div style="margin: 10px;">
	<div id="back_button" class="glyphicon glyphicon-backward btn btn-default control-button"></div>
	<div id="play_button" class="glyphicon glyphicon-play btn btn-default control-button"></div>
	<div id="volume_bar"> </div>
</div>

<div id="playlist" class="table table-condensed">
</div>

<script language="javascript">
var g_playlist = [
<?php
	$res = "";
	$path = './music';
	$dir = opendir($path);
	$first = true;
	while(false !== ($file = readdir($dir))){
		if($file != "." && $file != ".."){
			if(!is_dir($path."/".$file)){
				echo(sprintf("%s{url: '%s', name: '%s'}\n", $first?"":"," , urlencode($file), addslashes(substr($file, 0, strlen($file)-4))));
				$first = false;
				if(isset($_GET["q"])){
					$tmp = strpos($file, $_GET["q"]);
					if($tmp !== false){
						// get path of $file
						$res = "music/" . urlencode($file);
					}
				}
			}
		}
	}
	closedir($dir);
?>];
</script>
<script langauge="javascript">

function play(tar){
	tar = tar.replace(/\+/g, "%20");
	player.pause();
	setTimeout(function(){player.setAttribute("src", tar); player.play();}, 1000);
}

// player
player.addEventListener('ended', function(){
	this.play();
}, false);

player.addEventListener('pause', function(e){
	play_button.className = play_button.className.replace("glyphicon-pause", "glyphicon-play");
}, false);

player.addEventListener('play', function(){
	play_button.className = play_button.className.replace("glyphicon-play", "glyphicon-pause");
}, false);

player.addEventListener('timeupdate', function(){
	played_progress.style.width = (this.currentTime / this.duration) * 100 + '%';
}, false);

player.addEventListener('progress', function(){
	var endVal = this.seekable && this.seekable.length ? this.seekable.end(0) : 0;
	buffered_progress.style.width = (endVal / this.duration) * 100 + '%';
}, false);

// play_button
play_button.addEventListener('click' ,function(event){
	if(this.className.search("glyphicon-play") != -1){
		player.play();
	}
	else if(this.className.search("glyphicon-pause") != -1){
		player.pause();
	}
}, false);

// back_button
back_button.addEventListener('click', function(event){
	player.currentTime = 0;
}, false);

// progress_bar
progress_bar.addEventListener('click' ,function(event){
	player.currentTime =
	player.duration * (event.clientX - this.getBoundingClientRect().left) / this.clientWidth;
}, false);

// play-list
{
	var items = playlist.getElementsByTagName("div");
}

// volume_bar
{
	for(var i = 0 ; i < 12 ; i ++){
		volume_bar.innerHTML += "<div class='vbar vbar-on' style='margin-top: " + (21 - i) + "px;height: " + (10 + i) + "px'></div>";
	}
	volume_bar.addEventListener('click', function(e){
		var r = this.getBoundingClientRect();
		var bars = this.getElementsByTagName("div");
		for(i in bars){
			if(!(bars[i].getBoundingClientRect))
				continue;
			if(bars[i].getBoundingClientRect().left < e.clientX){
				bars[i].className = bars[i].className.replace("vbar-off", "vbar-on");
			}
			else{
				bars[i].className = bars[i].className.replace("vbar-on", "vbar-off");
			}
		}
		player.volume = (e.clientX - r.left + 0.0) / (r.right - r.left);

	});
}

{
	star.addEventListener('click', function(e){
		var old = document.getElementsByTagName("link")[1];
		var lnk = document.createElement("link");
		lnk.setAttribute("type", "text/css");
		lnk.setAttribute("rel", "stylesheet");
		lnk.setAttribute("href", "css/" + (old.href.search("night") != -1 ?"day":"night") + ".css");
		old.parentNode.replaceChild(lnk, old);
	});
}

{
	/* support single drag-drop currently */
	var g_movingTar = null;
	function cloneMouseEvent(e){
			var e2 = document.createEvent("MouseEvents");
			e2.initMouseEvent(e.type, true, true, window, 1, e.screenX, e.screenY, e.clientX, e.clientY,
        						e.ctrlKey, e.altKey, e.shiftKey, e.metaKey, 0, null);
			return e2;
	}
	bdy.addEventListener('mousemove', function(e){
		if(g_movingTar){
			// offset 50, 50
			g_movingTar.style.left = (e.clientX + 20) + "px";
			g_movingTar.style.top = (e.clientY + 10) + "px";
			if(!e.in_p && playlist.activePlacer){
				playlist.handleMouseExit();
			}
		}
	});
	bdy.addEventListener('mouseup', function(e){
		if(playlist.pressTimer) clearTimeout(playlist.pressTimer);
		/*if(g_movingTar){
			g_movingTar.dispatchEvent(cloneMouseEvent(e));
		}*/
	});


	function createSeparator(){
		//echo "<div class='playitem-separator'></div>";
		var x = document.createElement("div");
		x.className = "playitem-separator";
		return x;
	}
	var prev_play_item = null;
	function createPlayItem(name, url){
		var x = document.createElement("div");
		x.className = "playitem playable";
		x.innerText = name;
		x.url = url;
		x.addEventListener('click', function(event){
			if(prev_play_item)
			{
				prev_play_item.className = prev_play_item.className.replace("playing-item", "");
				var text = prev_play_item.getElementsByTagName("marquee")[0].innerText;
				prev_play_item.innerText = text;
			}
			this.className = this.className + " playing-item";
			var text = this.innerText;
			this.innerHTML = "<marquee style='width: 300px;' direction='right'>" + text + "</marquee>";
			prev_play_item = this;
			play("music/" + this.url);
		});
		x.addEventListener('mousedown', function(e){
			if(!g_movingTar){
				if(playlist.pressTimer) clearTimeout(playlist.pressTimer);
				var div = this;
				playlist.pressTimer = window.setTimeout(function(){
					var p = div.parentNode;
					p.removeChild(div.previousSibling);
					p.removeChild(div);
					div.className = div.className + " moving";
					div.style.left = (e.clientX + 50) + "px";
					div.style.top = (e.clientY + 50) + "px";
					bdy.appendChild(div);
					g_movingTar = div;
					var e2 = document.createEvent("MouseEvents");
					e2.initMouseEvent("mousemove", true, true, window, 1, e.screenX, e.screenY, e.clientX, e.clientY,
										e.ctrlKey, e.altKey, e.shiftKey, e.metaKey, 0, null);
					bdy.dispatchEvent(e2);
				}, 1000);
			}
		});
		playlist.addEventListener('mousemove', function(e){
			e.in_p = true;
		});
		x.addEventListener('mousemove', function(e){
			if(g_movingTar){
				var x = createItemPlacer();
				x.active();
				if(playlist.activePlacer){
					console.log("Switch Placer");
					// replace itself with placer
					playlist.replaceChild(x, this);
					// replaced with previous placer
					if(playlist.activePlacer == playlist.lastChild)
					{
						console.log("prev placer is lastChild, insert a new placer");
						playlist.insertBefore(this, playlist.lastChild);
						playlist.insertBefore(createSeparator(), playlist.lastChild);
						playlist.lastChild.inactive();
					}
					else
					{
						console.log("replace with prev placer");
						playlist.replaceChild(this, playlist.activePlacer);
					}
					playlist.activePlacer = x;
				}
				else{
					console.log("First Enter Playlist, insertBefore");
					console.log(this.innerText);
					playlist.insertBefore(playlist.activePlacer = x, this);
					playlist.insertBefore(createSeparator(), this);
				}
				if(x.nextSibling.nextSibling == playlist.lastChild)
				{
					playlist.removeChild(playlist.lastChild); // placer
					playlist.removeChild(playlist.lastChild); // separator
					playlist.setLastPlacer();
				}
			}
		});
		// onmovelistener
		return x;
	}
	function createItemPlacer(){
		var x = document.createElement("div");
		x.className = "playitem placer-inactive";
		x.inactive = function(){
			this.className = this.className.replace("-active", "-inactive");
		};
		x.active = function(){
			this.className = this.className.replace("-inactive", "-active");
		};
		x.addEventListener('click', function(){
			if(g_movingTar){
				g_movingTar.parentNode.removeChild(g_movingTar);
				g_movingTar.className = g_movingTar.className.replace(" moving", "");
				var p = this.parentNode;
				if(this == p.lastChild){
					p.insertBefore(g_movingTar, this);
					p.insertBefore(createSeparator(), this);
					this.inactive();
				}
				else
					p.replaceChild(g_movingTar, this);
				g_movingTar = null;
			}
		});
		return x;
	}

	function createSeparator(){
		var x = document.createElement("div");
		x.className = "playitem-separator";
		return x;
	}
	/* playlist */

	playlist.addPlayItem = function(item){
		this.appendChild(createSeparator());
		this.appendChild(item);
	};

	playlist.setLastPlacer = function(){
		playlist.lastChild.addEventListener('mousemove', function(e){
			if(g_movingTar && playlist.activePlacer != this) (playlist.activePlacer = this).active();
		});
	};
	
	playlist.handleMouseExit = function(){
		var x = this.activePlacer;
		delete this.activePlacer;
		if(x == this.lastChild)
			x.inactive();
		else{
			this.removeChild(x.previousSibling); // separator
			this.removeChild(x);
		}
	};

	for(var idx in g_playlist){
		playlist.addPlayItem(createPlayItem(g_playlist[idx].name, g_playlist[idx].url));
	}
	playlist.addPlayItem(createItemPlacer());
	playlist.setLastPlacer();
}


</script>
<?php if($res != ""){ echo "<script>play('".$res."');</script>"; } ?>
</body>

</html>
