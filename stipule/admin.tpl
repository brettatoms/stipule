<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Stipule - Admin</title>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
  <meta name="MobileOptimized" />
  <style type="text/css">
    a {color: #00C}
    .action_box {background-color: #CCC; margin: 10px; padding: 10px}
    div#message {display: none;}
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
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
  <script type="text/javascript" src="/admin.js"></script>

</head>
<body>
  <h1>Stipule - Admin</h1>
  <div id="message">
  </div>

  <div class="action_box">
    <p>Upload Accessions</p>
    <form id="acc_upload" action="/admin" method="post" 
	  enctype="multipart/form-data"> 
      <input type="file" name="data" />
      <input type="hidden" name="action" value="upload_accessions" />
      <input type="submit" value="Upload" />	  
    </form>
  </div>

  <div class="action_box">
    <p>Upload Plants</p>
    <form id="plant_upload", action="/admin" method="post" 
	  enctype="multipart/form-data"> 
      <input type="file" name="data" />
      <input type="hidden" name="action" value="upload_plants" />
      <input type="submit" value="Upload" />	  
    </form>
  </div>

  <div class="action_box">
    <p>
      <form id="create_db" action="/admin" method="post" 
	    enctype="multipart/form-data">
	<input type="hidden" name="action" value="admin_create" />
	<input type="submit" value="Create database" />	
      </form>
    </p>
  </div>

  <p>
  <a href="/">Back</a>
  </p>
  
</body>
</html>
