namespace HousePriceAnalysis

module Analyses =
    open HousePriceReader
    open PostcodeReader
    open DataSet
    open Statistics
    open PGraphs
    open System
    open System.Linq

    type ShortPostcodeValue = {Eastings:float;Northings:float;Price:float}

    let RawHousePriceMap(priceFilter:HousePriceInfo -> bool) =
        SomeTransactions(priceFilter) 
            |> Seq.map (fun (p,h) -> (p.Eastings, p.Northings, h.Price) )
            |> PGraphs.HeatMap("House Prices in the UK")("East")("North")

    let QuantileHousePriceMap(ntile:int)(ntiles:int)(gridUnit:float)(priceFilter:HousePriceInfo -> bool) = 
        let PostcodeValue = SomeTransactions(priceFilter)
                                |> Seq.map (fun (p,h) -> {Eastings=Math.Round((float p.Eastings)/gridUnit,0)*gridUnit;Northings=Math.Round((float p.Northings)/gridUnit,0)*gridUnit;Price=float h.Price})
                                |> Seq.groupBy (fun p -> (p.Eastings,p.Northings))
                                |> Seq.map (fun (k,v) ->  (k, v |> Seq.map (fun p -> p.Price) |> Quantiles(ntiles)))
        let X = PostcodeValue |> Seq.map (fun ((e,n),h) -> (e,n,h.[ntile]))
        let title = String.Format("House Price Distribution in UK: quantile {0} of {1}",ntile,ntiles)
        printfn "quantile %d of %d" ntile ntiles
        HeatMap(title)("x")("y")(X)
        
    let HeatMapAnalysis(filter:HousePriceInfo -> bool)(mapBox:float) =
        let y = SomeTransactions(filter)
        let dataSet = y |> Seq.map (fun (p,h) -> (p.Eastings, p.Northings, h.Price) )
        printfn "Total distributions %A" (dataSet.Count())
        let quantileDataSet = dataSet |> CollateBy(fun (x,y,v) -> (Math.Round(x/mapBox,0)*mapBox,Math.Round(y/mapBox,0)*mapBox))(QuantileBy(fun (x,y,v) -> v)(2)(4))
        printfn "Geographic distributions %A" (quantileDataSet.Count())
        HeatMap("Median House Prices in the UK")("East")("North")(quantileDataSet.Select(fun((x,y),v)->(x,y,v)))

    let BoxAnalysis(priceFilter:HousePriceInfo -> bool)(boxGrouper:HousePriceInfo -> string) =

        SomeTransactions(priceFilter)
            |> Seq.groupBy (fun (p,h) -> boxGrouper(h))
            |> Seq.map (fun (k,v) ->  (k, v |> Seq.map (fun (p,h) -> float h.Price) |> Quantiles(4)))
            |> Seq.sortByDescending (fun (c,q) -> q.[2])
           
    
    
    type BoxTableEntry = {Group:string;Quantile0:float;Quantile1:float;Quantile2:float;Quantile3:float;Quantile4:float}
    
    let BoxTableAnalysis(priceFilter:HousePriceInfo -> bool)(boxGrouper:HousePriceInfo -> string) =
    
        BoxAnalysis(priceFilter)(boxGrouper)
            |> Seq.map(fun (c,q) -> {Group=c;Quantile0=q.[0];Quantile1=q.[1];Quantile2=q.[2];Quantile3=q.[3];Quantile4=q.[4]})
            |> Util.Table
        
    let BoxPlotAnalysis(priceFilter:HousePriceInfo -> bool)(boxGrouper:HousePriceInfo -> string) =
    
        BoxAnalysis(priceFilter)(boxGrouper)
            |> BoxPlot("UK Property Price Distributions")("Property Price (£)")