$(function () {
    /* Global Page Adjuster */
    $(window).on('resize', function () {
        adjustPage();
    });

})

// var BASE_URL = window.location.origin + "/";
var BASE_URL = "http://192.168.1.130:5000/";
var processingSpinner = `<div class="spinner-border spinner-border-sm" role="status"> <span class="sr-only">Processing...</span> </div>`;

var keydownDBcer;

var map = { 18: false, 76: false, 83: false, 72: false, 78: false, 68: false, 84: false, 65: false, 82: false, 70: false, 69: false, 80: false, 67: false, 71: false, 9: false };
$(document).keydown(function (e) {
    map[76] = false;
    if (e.keyCode in map) {
        map[e.keyCode] = true;
        if (map[18] && map[83]) { //Alt + S KeyCode    **SUBMITS FORM**
            $('div.modal').hasClass('show') ? $("div.modal.show button[type=submit]").trigger("click") : '';
        } else if (map[18] && map[78]) { // Alt + N    **ADD NEW MODAL**  
            $("#modalAddNew").modal("show");
        } else if (map[18] && map[68]) { // Alt + D    **SAVE & ADD NEW**  
            $('#modalAddNew').hasClass('show') ? $("#AddSaveNew").trigger("click") : '';
            e.preventDefault();
        } else if (map[18] && map[84]) { // Alt + T    **FOCUS ON FIRST ELEMENT OF FORM**
            $('div.modal.show .modal-body *:input[type!=hidden]:first').focus();
        } else if (map[18] && map[82]) { // Alt + R    **Focus on Searchbox**
            $("#tblDBTable_filter input[type=search]").focus();
        } else if (map[18] && map[70]) { // Alt + F    **Fix Header**
            $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
            e.preventDefault();
        } else if (map[18] && map[69]) { // Alt + E    **Show entries**
            $('[name=tblDBTable_length]').focus();
            e.preventDefault();
        } else if (map[18] && map[72]) { //Alt + H  **HELP TOAST**
            showToast(`Esc = Close popup.<br>Alt + S = Submit/Confirm form.<br>Alt + D = Save & Add New.<br>Alt + N = Add New popup.<br>Alt + T = Focus on form.<br>
                            Alt + R = Focus on searchbar.<br>Alt + F = Fix Table Header.<br>Alt + E = Focus on show entries.<br>
                            Alt + G = Go Back.`, "info");
        } else if (map[18]) { //Alt key prevent default
            e.preventDefault();
        }
    }

}).keyup(function (e) {
    if (e.keyCode in map) {
        map[e.keyCode] = false;
    }
});

function adjustPage() {

    var winSize = ($(window).width() < 767 ? "sm" : "lg");

    let DTtable = "#tblDBTable";

    if ($("#tblDBTable").length) {
        $("#tblDBTable_filter label input").attr('placeholder', 'Search');
        $("#tblDBTable_wrapper div div.col-sm-12.col-md-6").removeClass("col-sm-12");

        $(DTtable).on('processing.dt', function (e, settings, processing) {
            if (processing) {
                $('#tblDBTableCard').block();
            } else {
                $('#tblDBTableCard').unblock();

            }
        }).dataTable();

        $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
        $('div#tblDBTable_length.dataTables_length label').contents().filter(function () { return this.nodeType === 3; }).remove();
        $("#tblDBTable_length label .toggle .toggle-group label").addClass("pl-1 pr-1 text-center");

    }

    switch (winSize) {
        case "sm":
            $(".modal-body table:not(.custom-table)").css('font-size', '0.7rem');
            $("div.scroll-sidebar.ps-container.ps-theme-default").addClass("ps-active-y");
            if ($("#main-wrapper").hasClass("show-sidebar")) {
                $("div.page-wrapper").css('filter', 'blur(3px)');
            }
            if ($("#tblDBTable").length) {
                $("div.page-wrapper, div.page-wrapper select, div.page-wrapper input, div.page-wrapper button ").css({ 'font-size': '0.7rem' });
                $("div.col-12.align-self-center h3").css('font-size', '1rem');
                $("div.page-breadcrumb div.row div.d-flex.align-items-center nav ol").css('font-size', '0.7rem');

                $("#tblDBTable_length label .toggle .toggle-group label").css('font-size', '0.7rem').contents().filter(function () { return this.nodeType === 3; }).remove();
                $("#tblDBTable_length label .toggle").css('font-size', '0.7rem').css('width', '0.7rem');

                $('div#tblDBTable_length.dataTables_length label').contents().filter(function () { return this.nodeType === 3; }).remove();


            }
            if (!$("#orgProfileRow").length && !$("#userProfileRow").length) {

                $("#navbarSupportedContent").prependTo('nav.sidebar-nav');
                $(`<div class="row" id="orgProfileRow"></div>`).appendTo("#navbarSupportedContent");
                $(`<div class="row" id="userProfileRow"></div>`).appendTo("#navbarSupportedContent");
                $("#navbarSupportedContent").addClass('show');
                $("#orgProfileCol").appendTo('#userProfileRow');
                $("#userProfileCol").appendTo('#orgProfileRow');
                $("#userProfileCol ul.navbar-nav.float-right").removeClass("float-right");
                $("ul.navbar-nav.float-left.mr-auto.ml-4.pl-1.w-100").removeClass("ml-4");
                $("div.dropdown-menu.dropdown-menu-right.user-dd.animated.flipInY").addClass('w-100');
                $("div.dropdown-menu.dropdown-menu-right.user-dd.animated.flipInY").removeClass("dropdown-menu-right");
                $("nav.sidebar-nav").css('padding-top', '2%');
            }
            break;
        case "lg":
            $(".modal-body table:not(.custom-table)").css('font-size', '1rem');
            $("div.scroll-sidebar.ps-container.ps-theme-default").removeClass("ps-active-y");
            $("div.page-wrapper").css('filter', '');
            if ($("#tblDBTable").length) {
                $("div.page-wrapper, div.page-wrapper select, div.page-wrapper input, div.page-wrapper button").css({ 'font-size': '1rem' });
                $("div.col-12.align-self-center h3").css('font-size', '1.3125rem');
                $("div.page-breadcrumb div.row div.d-flex.align-items-center nav ol").css('font-size', '1rem');

                $("#tblDBTable_length label .toggle .toggle-group label").css('font-size', '1rem');
                $("#tblDBTable_length label .toggle").css('font-size', '1rem').css('width', '113.125px');

                if (!$("#tblDBTable_length label .toggle").length) {
                    $('#tblDBTable_length label').prepend('Show ');
                    $('#tblDBTable_length label').append(' entries');
                } else {
                    $('#tblDBTable_length .toggle-group .toggle-on').append(' Open');
                    $('#tblDBTable_length .toggle-group .toggle-off').append(' Archived');
                }
            }
            if ($("#orgProfileRow").length && $("#userProfileRow").length) {

                $("#orgProfileCol").appendTo('#navbarRow');
                $("#userProfileCol").appendTo('#navbarRow');
                $("#navbarRow").appendTo("#navbarSupportedContent");
                $("#userProfileCol ul.navbar-nav").addClass("float-right");
                $("ul.navbar-nav.float-left.mr-auto.pl-1.w-100").addClass("ml-4");
                $("div.dropdown-menu.user-dd.animated.flipInY.w-100").addClass("dropdown-menu-right");
                $("div.dropdown-menu.dropdown-menu-right.user-dd.animated.flipInY.w-100").removeClass('w-100');
                $("#navbarSupportedContent").appendTo('#topnavbarnav');
                $("nav.sidebar-nav").css('padding-top', '30px');
                $("#orgProfileRow").remove();
                $("#userProfileRow").remove();
            }
            break;
    }

    $('#tblDBTable').on('click', 'tr td', function (e) {
        if ($(e.target).closest('div.actionCol').length == 0) {
            return;
        }
        $(this).click();
    });

}

let tblDataTable;

function CallBackHandler() {
    adjustPage();

    $("a").tooltip({ container: 'body' });

    setTimeout(function () {
        $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
    }, 100);

}

function InitCompleteHandler() {
    $("#tblDBTableCard").unblock();
    $('div.dataTables_filter input').attr('maxlength', 100).unbind().bind('keyup', function (e) {
        if (e.keyCode == 13) {
            FilterDTTable();
        }
    });
    let appendEl = $(`div.dataTables_filter label`);
    let btnSearch = `<button class="btn btn-primary" onClick="FilterDTTable();" style="margin-left: 1.5%"><i class="fas fa-search"></button>`;
    let btnRefresh = `<button class="btn btn-warning" onClick="FilterDTTable(true);" style="margin-left: 1.5%"><i class="fas fa-sync-alt"></button>`;
    let btnSettings = `<a href="javascript:;" title="Fix table header" data-placement="left" class="mr-2 my-2" onclick="$($.fn.dataTable.tables(true)).DataTable().columns.adjust();"><i class="fas fa-wrench text-primary"></i></a>`;
    appendEl.append(btnSearch).append(btnRefresh).prepend(btnSettings);

}

function ReloadDatatable(tblName = "#tblDBTable", reset = false, callback = null) {
    $(tblName).DataTable().ajax.reload(callback, reset);
}

function FilterDTTable(reset) {

    let searchBar = $("#tblDBTable_filter input[type=search]");
    if (reset) {
        searchBar.val("");
    }

    tblDataTable.fnFilter(searchBar.val());

}

function PopulateSelectMultiple(selectId, url, placeholder, allowClear, delay) {
    setTimeout(function () {
        $.ajax({
            url: BASE_URL + url,
            type: 'GET',
            success: function (resp) {
                let returndata = JSON.parse(resp);
                $('#' + selectId).select2({
                    placeholder: placeholder,
                    allowClear: allowClear
                });
                for (let i = 0; i < returndata.length; i++) {
                    var newOption = $(`<option value="` + returndata[i][0] + `" data-id-raw="` + returndata[i][1] + `">` + returndata[i][2] + `</option>`);
                    $('#' + selectId).append(newOption).trigger('change');
                }
            }
        });
    }, delay);

}

function delayFunction(functionName, Time) {
    eval(`setTimeout(function () {
        `+ functionName + `
    }, `+ Time + `);`);
}

function AddSelectMultiple(selectId, dataArr) {
    let tempArr = [];
    for (let i = 0; i < dataArr.length; i++) {
        let val = $("[id=" + selectId + "] *[data-id-raw='" + dataArr[i] + "']").val();
        tempArr.push(val);
    }
    $("[id=" + selectId + "]").val(tempArr).trigger('change');
    // $('#' + selectId).append(val).trigger('change');
}

function ClearSelectMultiple(selectId) {
    $('#' + selectId).val(null).trigger('change');
}

function PopulateSelect(name, url, placeholder, value, search, dataIN, prepend) {

    let promise = undefined;

    if (!$("[name=" + name + "] option").length) {

        promise = $.ajax({
            url: BASE_URL + url,
            type: 'GET',
            data: dataIN,
            success: function (resp) {
                let data = JSON.parse(resp);

                try {

                    if (data[0].length > 2) {
                        for (var i = 0; i < data.length; i++) {
                            let metaData = ``;
                            for (let j = 3; j < data[i].length; j++)
                                metaData += `data-meta-` + j + `= ` + `"` + data[i][j] + `"`;

                            var newOption = $(`<option value="` + data[i][0] + `" data-id-raw="` + data[i][1] + `" ` + metaData + ` >` + data[i][2] + `</option>`);
                            $("[name=" + name + "]").append(newOption);
                        }
                    } else {
                        for (var i = 0; i < data.length; i++) {
                            var newOption = $(`<option value="` + data[i][0] + `" data-id-raw="` + data[i][1] + `">` + data[i][2] + `</option>`);
                            $("[name=" + name + "]").append(newOption);
                        }
                    }


                } catch (e) {
                    showToast(`No data available for ` + url + ` dropdown.`, 'warning');
                    // return;
                }

                $("#" + name + "-spinner").css("display", "none");
                $("[name=" + name + "]").val("");
                $("[name=" + name + "]").css("display", "block");

                if (search) {

                    if (prepend) {
                        $("[name=" + name + "]").prepend(prepend);
                    } else {
                        $("[name=" + name + "]").prepend("<option></option>");
                    }

                    $("[name=" + name + "]").select2({
                        placeholder: placeholder,
                        minimumResultsForSearch: (0),
                        escapeMarkup: function (markup) { return markup; }
                    });
                } else {
                    $("[name=" + name + "]").addClass("form-control");
                    $("[name=" + name + "]").prepend("<option value='' selected disabled hidden>" + placeholder + "</option>")
                }

                if (value != null) {
                    let val = $("[name=" + name + "] *[data-id-raw='" + value + "']").val();
                    $("[name=" + name + "]").val(val).trigger('change.select2');
                    if (!val) {
                        showToast(`Cannot find ` + value + ` value on select2 ` + name, 'error');
                        $("[name=" + name + "]").select2("val", "");
                        $("[name=" + name + "]").val("").trigger("change");
                    }
                }

            }
        });
    } else {
        if (value != null) {
            let val = $("[name=" + name + "] *[data-id-raw='" + value + "']").val();
            $("[name=" + name + "]").val(val).trigger('change.select2');
            if (!val) {
                showToast(`Cannot find ` + value + ` value on select2 ` + name, 'error');
                $("[name=" + name + "]").select2("val", "");
                $("[name=" + name + "]").val("").trigger("change");
            }
        }
        $("#" + name + "-spinner").css("display", "none");
    }

    return promise;
}

function showToast(text, type) {

    $.toast({
        text: (type == "error" ? `<span>` + text + `<i class="far fa-copy ml-1 copyErrMsg" data-toggle="tooltip" title="Copy error message" style="cursor: pointer"></i></span>` : text),
        showHideTransition: 'slide',
        icon: type,
        position: 'bottom-right',
        hideAfter: (type == "error" && "info" ? 15000 : 7000),
    });

    $(".copyErrMsg").unbind().on('click', function () {
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val($(this).parent().text()).select();
        document.execCommand("copy");
        $temp.remove();
    });

}

function SerializeForm(form) {
    let result = {};
    $.each($(form).serializeArray(), function () {
        result[this.name] = this.value;
    });

    return JSON.stringify(result);

}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    return vars;
}

function getUrlParam(parameter, defaultvalue) {
    var urlparameter = defaultvalue;
    if (window.location.href.indexOf(parameter) > -1) {
        urlparameter = getUrlVars()[parameter];
    }
    return decodeURI(urlparameter);
}

function Numify(data) {
    let val = data;
    if (!Number.isNaN(parseFloat(data))) {
        val = parseFloat(data).toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
    }

    return val;
}