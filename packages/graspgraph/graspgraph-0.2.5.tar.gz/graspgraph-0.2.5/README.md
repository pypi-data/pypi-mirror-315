# graspgraph
Create easy-to-understand graphs

## Concept
Make it easier to understand with graphs

### Stats
![](./images/stats/usage.png)

### Database ER diagram-like
![](./images/dber/usage.png)

## What is possible
### statsgraph
1. Graphing statistics

### dbergraph
1. Graphing database table definition information

## Reason for development
- I want to make things that are difficult to understand through text alone easier to understand by creating graphs

## Versions

|Version|Summary|
|:--|:--|
|0.2.5|Refactoring|
|0.2.4|Add dbergraph|
|0.1.0|Release graspgraph(statsgraph)|

## Installation
### [graspgraph](https://pypi.org/project/graspgraph/)
`pip install graspgraph`

### [Graphviz](https://graphviz.org/download/)
Required for PDF output

### [Poppler](https://github.com/Belval/pdf2image?tab=readme-ov-file)
Required for PDF image conversion

## Usage
### statsgraph
![](./images/stats/usage.png)
```python
import graspgraph as gg

statsgraph = gg.Statsgraph(
  gg.StatsgraphAxis([1, 2, 3, 4, 5]),
  gg.StatsgraphAxis([11, 12, 13, 14, 15]),
  gg.FigureColors(line = "blue"))
figure = statsgraph.to_figure()
figure.LayoutTitleText = "<b>[statsgraph]<br>タイトル</b>"
figure.XTitleText = "X軸"
figure.YTitleText = "Y軸"
figure.Write("./statsgraph.png")
```

### dbergraph
![](./images/dber/usage.png)
```python
import graspgraph as gg

prefix = "./database"
dbergraph = gg.Dbergraph(gg.Database.from_file_path(gg.Path.join(prefix, "yaml")))
dbergraph.Database.update()
dot = dbergraph.to_dot()
dot.TitleText = "<b>[dbergraph]</b>"
pdfFilePath = gg.Path.join(prefix, "pdf")
pngFilePath = gg.Path.join(prefix, "png")
dot.Write(pdfFilePath)
gg.Pdf.convert(pdfFilePath, pngFilePath)
```

## CLI
### pdf.convert
Convert PDF to image

#### 1. Image(PNG) conversion by CLI execution
`graspgraph pdf.convert graph.pdf graph.png`
