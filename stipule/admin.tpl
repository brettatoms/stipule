<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Stipule - Admin</title>
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
<body>
  <h1>Stipule - Admin</h1>
  <div>
    {{ message }}
  </div>
  <div>
	<p>Upload Accessions</p>
	<form action="/admin/upload?class=accession" enctype="multipart/form-data" 
	      method="post">
	  <input type="file" name="data" />
	  <input type="submit" value="Upload" />
	</form>
  </div>
  <div>
	<p>Upload Plants</p>
  </div>
  <div>
    <p>
    <a href="/admin/create">Create new database</a>
    </p>
  </div>

  <p>
  <a href="/">Back</a>
  </p>
  
</body>
</html>
