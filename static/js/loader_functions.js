var left = BoxRegister.newBox();
var center = BoxRegister.newBox();
var right = BoxRegister.newBox();
var navigation = null;

var position = 0;
var endPosition = 0;

$(window).bind('popstate',Controller.stateHandler);
// window.onpopstate = Controller.stateHandler;

$(document).ready(load);

function previous() {
    if ( position == 0 ) {
        return;
    }
    position--;
    loadPosition();
}

function next() {
    var stateobj = {"data":1};
    window.history.pushState(stateobj,"blubb","test/index.html");
    return;
    if ( position == endPosition ) {
        return;
    }
    position++;
    loadPosition();
}

function load(){
    navigation = $('#location');
    $(document).ajaxStart(function() {
        $('#loading').show();
    });
    $(document).ajaxStop(function() {
        $('#loading').hide();
    });
    
    center.show('center');
    left.show('left');
    right.show('right');

    $.get('/Codebar/tests.php?.json_loadText/topic.1/subtopic.1',function(json){
        console.log(json,this);
    },'json');

    loadPosition();
}

function loadImprint() {
    right.empty();
    center.empty();
    left.empty();
    navigation.empty();
    
    loadCenterData(jsonData.imprint);
}

function loadPosition() {
    right.empty();
    center.empty();
    left.empty();
    navigation.empty();
    
    switch ( position ) {
        case 0:
            loadMicroBlogging();
            loadCenterData(jsonData.topicList);
        break;
        case 1:
            loadMicroBlogging();
            loadCenterData(jsonData.subTopicList);
            appendLeftData(jsonData.topicList);
            loadNavigation(["Wahlprogramm"]);
        break;
        case 2:
            loadMicroBlogging();
            loadCenterData(jsonData.subSubTopicList);
            appendLeftData(jsonData.topicList);
            appendLeftData(jsonData.subTopicList);
            loadNavigation(["Wahlprogramm","Umwelt und Verbraucherschutz"]);
        break;
        case 3:
            loadMicroBlogging();
            loadCenterData(jsonData.subSubSubTopicList);
            appendLeftData(jsonData.topicList);
            appendLeftData(jsonData.subTopicList);
            appendLeftData(jsonData.subSubTopicList);
            loadNavigation(["Wahlprogramm","Umwelt und Verbraucherschutz","Wasserwirtschaft"]);
        break;
        case 4:
            loadMicroBlogging();
            loadCenterData(jsonData.subSubSubSubTopicOverview);
            appendLeftData(jsonData.topicList);
            appendLeftData(jsonData.subTopicList);
            appendLeftData(jsonData.subSubTopicList);
            appendLeftData(jsonData.subSubSubTopicList);
            loadNavigation(["Wahlprogramm","Umwelt und Verbraucherschutz","Wasserwirtschaft","Abwasser"]);
        break;
        case 5:
            loadMicroBlogging();
            loadCenterData(jsonData.subSubSubTopicList);
            appendLeftData(jsonData.topicList);
            appendLeftData(jsonData.subTopicList);
            appendLeftData(jsonData.subSubTopicList);
            loadNavigation(["Wahlprogramm","Umwelt und Verbraucherschutz","Wasserwirtschaft"]);
        break;
        case 6:
            loadMicroBlogging();
            loadCenterData(jsonData.subSubSubTopicList);
            appendCenterData(jsonData.subSubSubTopicOverview);
            appendLeftData(jsonData.topicList);
            appendLeftData(jsonData.subTopicList);
            appendLeftData(jsonData.subSubTopicList);
            loadNavigation(["Wahlprogramm","Umwelt und Verbraucherschutz","Wasserwirtschaft"]);
        break;
    }
    
    endPosition = 6;
    
    document.getElementById('position').innerHTML = position + '/' + endPosition;
    
    // loadCenterTopicOverview();
    // loadLeftHistory();
}

function loadCenterData(json) {
    center.empty();
    appendCenterData(json,true);
}

function appendCenterData(json, append) {
    if ( append == null || append == undefined ) {
        append = true;
    } else {
        append = null;
    }
    var data = new ClassData();
    data.load(json);
    center.printData(data, append);
}

function appendLeftData(json) {
    var box4 = BoxRegister.newBox();
    box4.show('swap',left);
    
    data = new ClassData();
    data.load(json);
    box4.printData(data);
}

function loadNavigation(json) {
    for ( j in json ) {
        $('<li class="button" style="z-index: 501; position: relative;">' + json[j] + '</li>')
            .appendTo(navigation);
    }
}

function loadMicroBlogging() {
    right.empty();
    
    json = {"loadMicroBloggingResponse":[{"microBlogText":"Testblog 1.","microBlogID":1,"microBlogTime":1357746204,"authorGroup":[{"displayName":"author1"}]},{"microBlogText":"Testblog 2.","microBlogID":2,"microBlogTime":1357746304,"authorGroup":[{"displayName":"author2"}]}]};
    data = new ClassData();
    data.load(json);
    right.printData(data);
}

var jsonData = {
    "topicList" : {"loadIndexResponse":[{"shortTitle":"topic","index":1,"fullTitle":"<h2>Wahlprogramm</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]},{"shortTitle":"topic","index":2,"fullTitle":"<h2>Grundsatzprogramm</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]},{"shortTitle":"topic","index":3,"fullTitle":"<h2>Satzung</h2>","authorGroup":[{"displayName":"author1"}]}]}
    ,"subTopicList" : {"loadIndexResponse":[{"shortTitle":"subtopic","index":1,"fullTitle":"<h2>Umwelt und Verbraucherschutz</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]},{"shortTitle":"subtopic","index":2,"fullTitle":"<h2>Wirtschaft</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}]}
    ,"subSubTopicList" : {"loadIndexResponse":[
        {"shortTitle":"subsubtopic","index":1,"fullTitle":"<h2>Nachhaltigkeit</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]}
        ,{"shortTitle":"subsubtopic","index":2,"fullTitle":"<h2>Energieversorgung</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"shortTitle":"subsubtopic","index":3,"fullTitle":"<h2>Klimawandel</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"shortTitle":"subsubtopic","index":4,"fullTitle":"<h2>Wasserwirtschaft</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
    ]}
    ,"subSubSubTopicList" : {"loadIndexResponse":[
        {"shortTitle":"subsubtopic","index":1,"fullTitle":"<h2>Trinkwasser</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author2"}]}
        ,{"shortTitle":"subsubtopic","index":2,"fullTitle":"<h2>Abwasser</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"shortTitle":"subsubtopic","index":3,"fullTitle":"<h2>Gewässerschutz</h2>","authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
    ]}
    ,"subSubSubSubTopicOverview" : {"loadTextResponse":{"paragraphs":[{"wikiText":"<h2>Abwasser</h2>Abwasser ist ein Wertstoff und wir streben einen ressourcenschonenden Umgang mit den wertvollen Inhaltsstoffen an. Wir treten für die Abschaffung des Anschlusszwanges für häusliche Abwässer an das Abwassernetz ein, wenn die Einhaltung der Ablaufparameter nach der EU-Rahmenrichtlinie eigenverantwortlich sichergestellt wird. Industrielle und die von Krankenhäusern stammende Abwässer sind geeignet vorzubehandeln. Vermischung mit häuslichen Abwässern ist zu vermeiden.","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}],"isFollowing":1}}
    ,"subSubSubTopicOverview" : {"loadTextResponse":{"paragraphs":[
        {"wikiText":"<h2>Trinkwasser</h2>Wasser ist ein kommunales Gut und muss jedem Bürger zur Verfügung stehen. Wir stehen für die Rekommunalisierung der Wasserversorgung ein, da sie als Infrastruktur der Grundversorgung dient. Wir streben eine hohe Trinkwasserqualität an und wollen diese auch durch die Reduzierung von Schadstoffeintrag erreichen. Die Trinkwasserverordnung soll an aktuelle Erkenntnisse über Wasserinhaltsstoffe regelmässig angepasst werden. Die Eigenwasserversorgung privater Haushalte soll grundsätzlich erlaubt sein. Sofern eine private Hauswasserversorgung möglich ist, lehnen wir einen Anschlusszwang an das kommunale Trinkwassernetz ab. Die Qualitätsprüfung ist eigenverantwortlich zu leisten. ","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"wikiText":"<h2>Abwasser</h2>Abwasser ist ein Wertstoff und wir streben einen ressourcenschonenden Umgang mit den wertvollen Inhaltsstoffen an. Wir treten für die Abschaffung des Anschlusszwanges für häusliche Abwässer an das Abwassernetz ein, wenn die Einhaltung der Ablaufparameter nach der EU-Rahmenrichtlinie eigenverantwortlich sichergestellt wird. Industrielle und die von Krankenhäusern stammende Abwässer sind geeignet vorzubehandeln. Vermischung mit häuslichen Abwässern ist zu vermeiden.","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
        ,{"wikiText":"<h2>Gewässerschutz</h2>Die Wasserressourcen sind von Beeinträchtigungen freizuhalten. In allen Bereichen müssen Eingriffe in den Boden auf ihre Verträglichkeit mit dem Gewässerschutz hin überprüft und gegebenenfalls angepasst werden. ","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}
    ],"isFollowing":1}}
    ,"imprint" : {"loadTextResponse":{"paragraphs":[{"wikiText":"<h2>Impressum</h2>Angaben gemäß § 5 TMG:<br>\r\n<br>\r\nKrohlas & Wingert IT GbR<br>\r\n<br>\r\nHauptstraße 91<br>\r\n<br>\r\n76706 Dettenheim<br>\r\n<br>\r\n<br>\r\n<br>\r\n<br>\r\nVertreten durch: Sven Krohlas, Justus Wingert<br>\r\n<br>\r\nIhr Ansprechpartner für Fragen jeder Art: Justus Wingert <a href=\"mailto:justus_wingert@web.de\">justus_wingert@web.de</a>","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":[{"displayName":"author1"},{"displayName":"author3"}]}],"isFollowing":1}}
};














