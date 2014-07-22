/***
 *	Require:		jQuery
 *
 */

var Lrc = (function(){
	var reg_ti = /\s*\[\s*ti\s*:([^\]]*)\]/,
		reg_ar = /\s*\[\s*ar\s*:([^\]]*)\]/,
		reg_al = /\s*\[\s*al\s*:([^\]]*)\]/,
		reg_by = /\s*\[\s*by\s*:([^\]]*)\]/,
		reg_lr = /\s*\[([0-9]{2}):([0-9]{2})\.([0-9]{2})\](.*)/;

	// constructor
	var Parser = function(lyrics, outputHandler){
		var that = this, lines = lyrics.split("\n");
		function parseTo(reg, lines){
			for(var line, res; line = lines.shift() ;)
				if(res = reg.exec(line))
					return res;
			return false;
		}
		function seekIdx(sec){
			var idx = 0;
			for( ; idx+1 < lines.length && lines[idx+1].time < sec; idx ++);
			return idx;
		}
		function failed(str){
			this.start = this.rewind = this.stop = function(){console.error(str)};
		}
		if(!(that.ti = parseTo(reg_ti, lines))) return failed("can't get ti");
		if(!(that.ar = parseTo(reg_ar, lines))) return failed("can't get ar");
		if(!(that.al = parseTo(reg_al, lines))) return failed("can't get al");
		if(!(that.by = parseTo(reg_by, lines))) return failed("can't get by");
		for(var i = 0, res; i < lines.length ; i ++)
			if(res = reg_lr.exec(lines[i])){
				lines[i] = {
					time: parseInt(res[1])*60+parseInt(res[2])+parseInt(res[3])*0.01,
					line: res[4]
				};
			}
			else failed("parse lyric failed");
		var timeOutTick = null, idx = 0;
//		function timeOutFunc(){
//			outputHandler(lines[++idx].line);
//			if(idx+1<lines.length)
//				timeOutTick = setTimeout(timeOutFunc, (lines[idx+1].time - lines[idx].time)*1000);
//			else that.stop();
//		}
		this.update = function(sec){
//			if(idx < lines.length){
//				outputHandler(lines[idx].line);
//				if(idx+1<lines.length)
//					timeOutTick = setTimeout(timeOutFunc, (lines[idx+1].time - sec)*1000);
//			}
			if(lines[idx+1].time < sec){
				outputHandler(lines[++idx].line);
			}
		};
		this.seek = function(sec){
			idx = seekIdx(sec);
			outputHandler(line[idx].line);
		};
		this.stop = function(){
			//clearTimeout(timeOutTick);
		};
	};
	return Parser;
})();

function getLrc(callback, src){
	$.ajax({url: src, type: 'GET',
		xhr: function() {
			var myXhr = $.ajaxSettings.xhr();
			toggleProgressbar("<progress></progress>");
			if(myXhr.upload) myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
			return myXhr;
		},
		cache: false,
		contentType: false,
		processData: false
	})
	.done(function(html){
		callback(html);
		hiddenProgressbar();		
	});
}
