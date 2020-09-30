def plot_shapefile_map(shapefile, colorfield, cmap=plt.cm.inferno, use_polygons=False):
    labels=list(set((shape.record[colorfield] for shape in shapefile.shapeRecords())))
    colormap={x:y for x,y in zip(labels,cmap([i/len(labels) for i in range(len(labels))]))}
    
    xs={label:[] for label in labels}
    ys={label:[] for label in labels}
    
    for shape in shapefile.shapeRecords():
        x,y = zip((*shape.shape.points))
        xs[shape.record[colorfield]]+=x
        xs[shape.record[colorfield]]+=[None]
        ys[shape.record[colorfield]]+=y
        ys[shape.record[colorfield]]+=[None]
    
    for label in labels:
        if use_polygons:
            plt.fill(xs[label],
                     ys[label], 
                     facecolor=colormap[label],
                     label=label,
                     alpha=0.5)
        else:
            plt.plot(xs[label],
                     ys[label],
                     c=colormap[label],
                     label=label,
                     linewidth=0.5)

            
                
#     with sf.Writer(output_filepath) as w:
#         for i,f in enumerate(glob.glob(input_filepaths)):
#             r=sf.Reader(f,encoding='Latin')
#             if i==0:
#                 w.fields = r.fields
#             for s in r.iterShapeRecords():
#                 if (xlim is None and ylim is None) \
#                     or any([x>xlim[0] and x<xlim[1] and y>ylim[0] and y<ylim[1] for x,y in s.shape.points]):
#                     w.shape(s.shape)
#                     w.record(*s.record)