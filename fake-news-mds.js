jQuery.fn.on;
var APP = APP || {};
APP.completeFile = "Fake-news-original-with-nonEnglish.csv";
APP.fakeFill = "red";
APP.trustworthyFill = "green";
APP.unknownFill = "blue";
APP.distanceFactor = 25;
APP.translate = 0;
APP.textLengthMinRange = 5;
APP.textLengthMaxRange = 20;
APP.r = 1;
APP.plotComplete = async function () {
    APP.table = APP.table || await getTable();

    async function getTable() {
        var p = new Promise(async function (resolve, reject){
            var result = await d3.csv(APP.completeFile);
            result = result.map(function(d) {
                return {
                    Title: d.Title,
                    Author: d.Author,
                    Text: d.Text,
                    Description: d.Description,
                    URL: d.URL,
                    AdvertisementCount: Number(d.AdvertisementCount || 0),
                    UpdatedDate: Number(d.UpdatedDate),
                    PotentialFake: Number(d.PotentialFake),
                    NumberAuthor: Number(d.NumberAuthor || 0),
                    TitleLength: Number(d.TitleLength),
                    FullTextLength: Number(d.FullTextLength),
                    TextLength: Number(d.TextLength),
                    CapitalWordTitle: Number(d.CapitalWordTitle),
                    NumberOfQuotes: Number(d.NumberOfQuotes),
                    Title_sentiment: Number(d.Title_sentiment),
                    Text_sentiment: Number(d.Text_sentiment),
                    Description_sentiment: Number(d.Description_sentiment),
                    EmotionalLanguage: Number(d.EmotionalLanguage || 0)
                };
            });
            resolve(result);
        });
        return p;
    }
    console.log(APP.table);
    plot();

    function plot() {
        if (!APP.datatable) {
            $(document).ready(function() {
                function textAreaRenderer (data, type, row) {
                    var html = `
                        <textarea readonly>${data}</textarea>
                    `;
                    return html;
                }
                function largeTextAreaRenderer (data, type, row) {
                    var html = `
                        <textarea style="width:500px;" readonly>${data}</textarea>
                    `;
                    return html;
                }
                APP.datatable = $("#raw-data").DataTable({
                    data: APP.table,
                    dom: "Bfrtip",
                    buttons: ["colvis"],
                    drawCallback: function(settings) {
                        $(".table-check").on("change", function(e) {
                            var index = this.getAttribute("id").substr(12);
                            var elem = $(this);
                            var rowChecked = $(this).prop("checked");
                            var cir = $("#cir-" + index);
                            if (rowChecked) {
                                cir.addClass("user-point");
                            } else {
                                cir.removeClass("user-point");
                            }
                        });
                    },
                    columns: [
                        {
                            render: function(data, type, row) {
                                var html;
                                html = `<input class="table-check" id="table-check-${row.index}" type="checkbox">`;
                                return html;
                            }
                        },
                        { 
                            data: "AdvertisementCount",
                            title: "Advertisement Count",
                            visible: false
                        },
                        { 
                            data: "Author",
                            title: "Author",
                            render: textAreaRenderer,
                            visible: true
                        },
                        { 
                            data: "Description",
                            title: "Description",
                            render: textAreaRenderer,
                            visible: false
                        },
                        { 
                            data: "Description_sentiment",
                            title: "Description Sentiment",
                            visible: false
                        },
                        { 
                            data: "EmotionalLanguage",
                            visible: false,
                            title: "Emotional Language Frequency"
                        },
                        { 
                            data: "URL",
                            title: "URL",
                            render: function (data, type, row) {
                                return `<a href="${data}">${data}</a>`;
                            }
                        },
                        { 
                            data: "NumberOfQuotes",
                            title: "Quote Frequency",
                            visible: false
                        },
                        { 
                            data: "NumberAuthor",
                            visible: false,
                            title: "Number of Authors"
                        },
                        { 
                            data: "UpdatedDate",
                            visible: false,
                            title: "Updated Date"
                        },
                        { 
                            data: "Text",
                            title: "Text",
                            width: "25%",
                            render: largeTextAreaRenderer
                        },
                        { 
                            data: "Text_sentiment",
                            title: "Text Sentiment",
                            visible: false
                        },
                        { 
                            data: "Title",
                            title: "Title",
                            render: textAreaRenderer
                        }
                    ]
                });
            });
        }
        var tooltip = d3.select('body').append('div') .attr("class","tooltip").style("color", "blue")
            .style("background-color", "white").style("border", "1px solid black");

        var graph = TableToGraph();
        console.log(graph);

        var simulation = d3.forceSimulation(graph.vertices)
            .force("spring", d3.forceLink(graph.edges).distance(edge => APP.distanceFactor*(edge.distance + APP.translate))
                )
            .force("center", d3.forceCenter(400,300))
            .on("tick", ticked);

        var sentiments = APP.table.map(function(d) {
            return Number(d.TotalSentiment);
        });
        var sentimentScale = d3.scaleLinear().domain([d3.min(sentiments), d3.max(sentiments)]).range([5, 20]);
        var textLengths = APP.table.map(function(d) {
            return Number(d.FullTextLength);
        });
        var textLengthScale = d3.scaleLinear().domain([d3.min(textLengths), d3.max(textLengths)]).range([APP.textLengthMinRange, APP.textLengthMaxRange]);

        var svg = d3.select("#info-vis");
        var zoomLayer = svg.select("g");
        var zoomed = function() {
            zoomLayer.attr("transform", d3.event.transform);
          }
        svg.call(d3.zoom().on("zoom", zoomed));
        function ticked() {
            d3.select("g")
                .selectAll("circle")
                .data(graph.vertices)
                    .attr("cx", node => node.x)
                    .attr("cy", node => node.y)
                .enter().append("circle")
                    .attr("class", function(d, i) {
                        var classes = "points ";
                        if (d.addedByUser || d.checked) {
                            classes += "user-point";
                        }
                        return classes;
                    })
                    .attr("id", function(d, i) {
                        return "cir-" + d.index;
                    })
                    .attr("r", d => textLengthScale(d.FullTextLength || 0))
                    .attr("fill", function (d, i) {
                        var result = APP.unknownFill;
                        if (d.PotentialFake === 1) {
                            result = APP.fakeFill;
                        } else if (d.PotentialFake === 0) {
                            result = APP.trustworthyFill;
                        }
                        return result;
                    })
                    .on("mouseover", function (d, i) {
                        d3.select(this).classed("highlight", true);
                        tooltip.style('opacity', .9);
                        var author = d.Author;
                        var maxlen = 100;
                        var text = "";
                        if (d.Text) {
                            text = d.Text.substring(0, maxlen);
                        }
                        tooltip.html(`
                        <div><b>URL:</b> ${d.URL}</div>
                        <div><b>Updated Date:</b> ${d.UpdatedDate}</div>
                        <div><b>Advertisement Count:</b> ${d.AdvertisementCount}</div>
                        <div><b>Author:</b> ${author}</div>
                        <div><b>Capital Word Title:</b> ${d.CapitalWordTitle}</div>
                        <div><b>Description:</b> ${d.Description}</div>
                        <div><b>Description sentiment:</b> ${d.Description_sentiment}</div>
                        <div><b>Emotional Language Frequency:</b> ${d.EmotionalLanguage}</div>
                        <div><b>Full Text Length:</b> ${d.FullTextLength}</div>
                        <div><b>Number Of Quotes:</b> ${d.NumberOfQuotes}</div>
                        <div><b>Text:</b> ${text}...</div>
                        <div><b>Text Length:</b> ${d.TextLength}</div>
                        <div><b>Text sentiment:</b> ${d.Text_sentiment}</div>
                        <div><b>Title:</b> ${d.Title}</div>
                        <div><b>Title Length:</b> ${d.TitleLength}</div>
                        <div><b>Title sentiment:</b> ${d.Title_sentiment}</div>
                        `);
                    })
                    .on("mouseout", function (d, i) {
                        d3.select(this).classed("highlight", false);
                        tooltip.style('opacity', 0).style("top", "-100000000px");
                    })
                    .on("click", (d, i) => {

                        $("#details-ad-count").text(d.AdvertisementCount);
                        $("#details-author").text(d.Author);
                        $("#details-description").text(d.Description);
                        $("#details-description-sent").text(d.Description_sentiment);
                        $("#details-el-freq").text(d.EmotionalLanguage);
                        $("#details-full-text-len").text(d.FullTextLength);
                        $("#details-n-quotes").text(d.NumberOfQuotes);
                        $("#details-text").text(d.Text);
                        $("#details-text-len").text(d.TextLength);
                        $("#details-text-sent").text(d.Text_sentiment);
                        $("#details-title").text(d.Title);
                        $("#details-title-2").text(d.Title);
                        $("#details-title-sent").text(d.Title_sentiment);
                        $("#details-url").text(d.URL);
                        document.getElementById("details-url").href = d.URL;

                        $("#details-modal").modal("show");
                    })
                    .on("mousemove", function (d, i) {
                        tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px").style("color","blue");
                    });

            // Make text labels for dots:
            if ($("#show-url:checked").prop("checked")) {
                d3.select("g").selectAll("text")
                    .data(graph.vertices)
                        .attr("x", node => node.x)
                        .attr("y", node => node.y)
                        .attr("class", "small")
                        .text(function(node) {
                            var text = "";
                            var maxlen = 25;
                            if (node.URL) {
                                text = node.URL.substring(0, maxlen) + "...";
                            }
                            return text;
                        })
                    .enter().append("text");
            } else {
                $("text").remove();
            }
        }

        function TableToGraph() {
            var selectedAttributes = $(".attribute-selection input:checked")
                .map(function() {
                    return this.value;
                }).get();
            var graph = {'vertices':APP.table, 'edges':[], 'norms':{}, 'attrs': selectedAttributes};
            for (var attr of graph.attrs)
                graph.norms[attr] = d3.deviation(APP.table, row => row[attr]);
            APP.table.forEach( (src, isrc) =>
                APP.table.forEach( (dst, idst) => {
                    if(isrc < idst)
                        graph.edges.push( {'source': src, 'target': dst, 'distance': Distance(src,dst,graph.norms, APP.r)} );
            }));
            return graph;
        }

        function Distance(r1, r2, norms, r) {
            r = r || 1;
            console.log(r);
            return Math.pow(d3.sum(Object.keys(norms).map(attr => 
                Math.abs(Math.pow((r1[attr] - r2[attr])/norms[attr], r)))), 1/r);
        }
    }
}
APP.plotComplete();
$(document).ready(function() {
    $("#submit-article-btn").on("click", event => {
        var title = $("#article-title").val();
        var text = $("#article-text").val();
        var description = $("#article-description").val();
        var author = $("#article-author").val();
        var url = $("#article-url").val();
        var adCount = $("#article-ad-count").val();
        var updateDate = new Date($("#article-update-date").val()).getTime();
        var persist = $("#article-persist").prop("checked");
        var article = {
            title: title || " ",
            text: text || " ",
            description: description || " ",
            author: author || " ",
            url: url || " ",
            adCount: adCount || 0,
            updateDate: updateDate || 0,
            persist: persist || false
        };
        console.log(article);
        $("#add-article-modal").modal("hide");
        $.post("", article).done(jsonResponse => {
            console.log(jsonResponse);
           jsonResponse.Text = jsonResponse.text;
           jsonResponse.Author = jsonResponse.author;
           jsonResponse.Description = jsonResponse.description;
           jsonResponse.Title = jsonResponse.title;
           jsonResponse.AdvertisementCount = jsonResponse.ad_count;
           jsonResponse.UpdatedDate = jsonResponse.updated_date;
           jsonResponse.URL = jsonResponse.url;
           jsonResponse.EmotionalLanguage = jsonResponse.EmotionalLanguage || 0;
           jsonResponse.NumberAuthor = jsonResponse.NumberAuthor || 0;
           jsonResponse.addedByUser = true;
           APP.addArticle(jsonResponse);
        });
    });

    $(".attribute-selection input").on("click", event => {
        APP.plotComplete();
    });

    $("#distance").val(APP.distanceFactor);
    $("#r-value").val(APP.r);
    $(".parameter").on("change", function(event) {
        console.log("param");
        var distance = $("#distance").val();
        APP.distanceFactor = distance;

        var r = $("#r-value").val();
        APP.r = r;
        APP.plotComplete();
    });
    $(".table-check").on("change", function(e) {
        console.log("Im here");
    });
});


APP.addArticle = function (article) {
    APP.table.push(article);
    APP.datatable.row.add(article).draw();
    APP.plotComplete();
};