<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Stipule - Accession Search</title>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
  <meta name="MobileOptimized" />
  <style type="text/css">
    a {color: #00C}
  </style>
  <script type="text/javascript">
    var formInUse = false;
    function setFocus()
    {
      if(!formInUse) {
        document.search_form.q.focus();
    }
    }
  </script>
  <!-- <script type="text/javascript" src="http://www.google.com/jsapi"></script> -->
  <!-- <script type="text/javascript"> google.load("jquery", "1.3.2"); </script> -->
</head>
<body onload="setFocus()">
  {{!body}}
  <br />
  <form name="search_form" action="/search" method="get">
    <div>
      <input type="text" name="q" onfocus="formInUse=true;"/>
      <!-- <span style="margin-left: 30px"><a href="http://zxing.appspot.com/scan?ret=http://naplesbg.herokuapp.com/search?q={CODE}">scan</a></span> -->
      <span style="margin-left: 30px"><a href="zxing:///scan?ret=http://naplesbg.herokuapp.com/search?q%3d%7bCODE%7d">scan</a></span>
      <span style="margin-left: 30px"><a href="/static/map-current.png">view map</a></span>
      <br />
      <input type="submit" value="Search">
    </div>
  </form>
</body>
</html>
