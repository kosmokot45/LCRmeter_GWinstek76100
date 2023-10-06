### <b>Startup instructions</b>
___
To run the program, you need to create a virtual environment and install the necessary libraries into it; for this, the following commands are used in the terminal:
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements
```
It is not necessary to use a virtual environment, you can simply install the necessary libraries into the system

```
pip install -r requirements
```

To connect the device, select COM4, BR - 115200 and click "Connect".

Next, the parameters of the experiment are filled in.

After filling in the parameters, you must click "Apply", then all the parameters will be written to the program memory and the frequency steps will be calculated.

Next, you need to click "Start" and the experiment will begin.

When the experiment is completed, you can build a graph with the "Graph" button. If something has already been drawn in the chart windows, it will be erased. For example, if the model was drawn first.

To save the experiment data to a csv file, click "Save".

Model building in the "Model building" tab. Each new model is built on top of everything that was on the chart.

To clear the chart, click "Clear".

After clearing the graphs, you can re-display the experiment data (Graph, Experiment Progress tab) and model data (Graph, Model Building tab).

### To Do List:

- [ ] Median value of results
- [ ] Create class of "lcr-meter" and use it in gui
- [ ] New branch for async or mp gui
- [ ] Refac design