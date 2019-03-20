namespace HousePriceAnalysis

module PGraphs = 
    open XPlot.Plotly
    open Statistics
    open System.Linq
//
//    let FrequencyDistribution(title:string)(xlabel:string)(buckets:int)(dataSet:seq<float>) =
//        let maxValue = dataSet.Max()
//        let maxBucket = int ((maxValue/float buckets)-((maxValue/float buckets) % 1.0)) + 1
//        Chart.Column //  .Histogram(dataSet,Title=title,XTitle=xlabel,YTitle="Frequency",Intervals=float buckets)


    let ScatterPlot(title:string)(xlabel:string)(ylabel:string)(dataSet:seq<float*float>) =
        //let X = dataSet |> MatchBandsBy(10)(fun (x,y,z) -> z) |> Seq.map (fun ((x,y,z),i) -> (x,y))
        let g = Chart.Scatter(dataSet)
        g.WithTitle(title)
        g.WithXTitle(xlabel)
        g.WithYTitle(ylabel)
        g
    
    let HeatMap(title:string)(xlabel:string)(ylabel:string)(dataSet:seq<float*float*float>) =
        
        let data = Scattergl(x=(dataSet.Select(fun (X,Y,v) -> X)),
                             y=(dataSet.Select(fun (X,Y,v) -> Y)),
                             mode="markers",
                             marker=Marker(size=2.,
                                           color=(dataSet.Select(fun (X,Y,v) -> v)),
                                           colorbar=Colorbar())
                             )

        let layout = Layout(title = title,
                            width = 600.,
                            height = 600.,
                            xaxis = Xaxis(gridwidth=2.,
                                          title=xlabel),
                            yaxis = Yaxis(gridwidth=2.,
                                          title=ylabel)
                            )

        (data, layout)
            |> Chart.Plot
            //|> Chart.Show

    let BoxPlot(title:string)(ylabel:string)(dataSet:seq<string*array<float>>) =
        dataSet
            |> Seq.map(fun (c,q) -> Box(y=q, name=c))
            |> Chart.Plot
            |> Chart.WithLayout(Layout(title = title, 
                                        showlegend = true,
                                        yaxis=Yaxis(title=ylabel)))

//        let data = Scattergeo(lat=(dataSet.Select(fun (X,Y,v) -> X)),
//                             lon=(dataSet.Select(fun (X,Y,v) -> Y)),
//                             mode="markers",
//                             marker=Marker(size=2.,
//                                            color=(dataSet.Select(fun (X,Y,v) -> v)))
//                             )
//
//        let layout = Layout(title = title,
//                            width = 600.,
//                            height = 600.,
//                            xaxis = Xaxis(gridwidth=2.,
//                                          title=xlabel),
//                            yaxis = Yaxis(gridwidth=2.,
//                                          title=ylabel),
//                            geo=Geo(scope="europe",
//                                    showland=true,
//                                    showcountries=true)
//                            )