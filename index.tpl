<!doctype html>
<meta charset='utf-8' />
<meta name="viewport" content="width=device-width, user-scalable=no" />
<title>webdumpy</title>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link rel='stylesheet' href='{{ docroot }}/res/webdumpy.css' type='text/css'>
<script>
var documentRoot = "{{ docroot }}";
</script>
<form action='{{ docroot }}/do/upload' method='POST' enctype='multipart/form-data'>
    <div class='layout-bar layout-bar_regular'>
        <div class='layout-bar__fixed'>
            <label for='upfile' class='form-button form-button_regular' data-bind='upBtn'>
              Select files
            </label>
            <input type='file' name='files' id='upfile' data-bind='uploader' multiple>
            <span data-bind='upList' class='hidden'></span>
            <button type='submit' class='form-button form-button_regular'>
              Upload
            </button>
        </div>
        <div class='layout-bar__fluid'></div>
        <div class='layout-bar__fixed'>
            <a href='{{ docroot }}/do/logout' class='form-button form-button_accent'>Logout</a>
        </div>
    </div>
</form>
<form action='{{ docroot }}/do/delete' method='POST'>
    <table data-bind='tabulator'>
        <tr>
            <th></th>
            <th><a href='?sort=name' class='flink'>Name</th>
            <th><a href='?sort=type' class='flink'>Type</th>
            <th><a href='?sort=size' class='flink'>Size</a></th>
            <th>Actions</th>
        </tr>
    </table>
    <div class='layout-bar layout-bar_footer-fixed layout-bar_regular'>
        <div class='layout-bar__fixed'>
            <button type='submit' class='form-button form-button_accent'>
              Delete selected
            </button>
        </div>
        <div class='layout-bar__fluid'>
        </div>
    </div>
</form>
<div class='modal' data-bind='renameModal' onsubmit='renameValidation()'>
    <form action='{{ docroot }}/do/rename' method='POST'>
        <div class='modal__row'>
            <input type='hidden' name='source' data-bind='renameOld'>
            <div class='form-input'>
                <input class='form-input__input' type='text' name='target' data-bind='renameNew' id='renameNew'>
                <label class='form-input__label' for='renameNew'>Enter new name</label>
            </div>
        </div>
        <div class='modal__row modal__row_right'>
            <button type='submit' class='form-button form-button_regular'>
              Rename
            </button>
            <button type='button' class='form-button form-button_accent' onclick='renameHide()'>Close</button>
        </div>
    </form>
</div>
<script src='{{ docroot }}/res/webdumpy.js'></script>
