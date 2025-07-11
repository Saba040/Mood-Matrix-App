from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from collections import defaultdict

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.setParent(None)

def draw_bar_chart(layout, mood_productivity_avg):
    fig = Figure(figsize=(4, 3))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    moods = list(mood_productivity_avg.keys())
    avg_productivities = list(mood_productivity_avg.values())

    ax.bar(moods, avg_productivities, color='skyblue')
    ax.set_title("Average Productivity")
    ax.set_ylabel("Productivity")
    layout.addWidget(canvas)

def draw_line_chart(layout, mood_productivity_trend):
    fig = Figure(figsize=(4, 3))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    for mood, prod_values in mood_productivity_trend.items():
        prod_values.sort(key=lambda x: x[0])  # sort by date
        dates = [d for d, _ in prod_values]
        prod = [p for _, p in prod_values]
        ax.plot(dates, prod, label=mood, marker='o')

    ax.set_title("Productivity Over Time")
    ax.set_xlabel("")
    ax.set_ylabel("Productivity")
    ax.legend()
    layout.addWidget(canvas)

def draw_pie_chart(layout, mood_counts):
    fig = Figure(figsize=(4, 3))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    labels = list(mood_counts.keys())
    sizes = list(mood_counts.values())

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title("Mood Distribution")
    layout.addWidget(canvas)

def draw_all_charts(bar_layout, line_layout, pie_layout, tasks):
    clear_layout(bar_layout)
    clear_layout(line_layout)
    clear_layout(pie_layout)

    mood_totals = defaultdict(list)
    mood_trend = defaultdict(list)
    mood_counts = defaultdict(int)

    for task in tasks:
        # task = (id, task, mood, date, productivity)
        mood = task[2]
        date = task[3]
        productivity = task[4]

        mood_totals[mood].append(productivity)
        mood_counts[mood] += 1
        mood_trend[mood].append((date, productivity))

    # Calculate averages for bar chart
    mood_avg = {
        mood: sum(values)/len(values) if values else 0
        for mood, values in mood_totals.items()
    }

    draw_bar_chart(bar_layout, mood_avg)
    draw_line_chart(line_layout, mood_trend)
    draw_pie_chart(pie_layout, mood_counts)
