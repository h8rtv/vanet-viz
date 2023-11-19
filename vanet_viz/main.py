from argparse import ArgumentParser
import pyray as ray
import pandas as pd


class Node:
    def __init__(self, pos_x, pos_y, timestamp):
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.timestamp = timestamp


def parse_data(input_data: str, scale: int):
    data = pd.read_csv(input_data)[:100]
    cols = ['snd_pos_x', 'snd_pos_y', 'timestamp']
    nodes = [Node(x // scale, y // scale, timestamp)
             for _, (x, y, timestamp) in data[cols].iterrows()]

    return nodes


def run():
    arg_parser = ArgumentParser(
        prog='vanet-viz',
        description='Visualizer for VANETs as Temporal Graphs')

    arg_parser.add_argument('input_data')
    arg_parser.add_argument('--min', default=0)
    arg_parser.add_argument('--max', default=1500)
    arg_parser.add_argument('--scale', default=2)
    args = arg_parser.parse_args()

    nodes = parse_data(args.input_data, args.scale)

    render(width=(args.max) // args.scale,
           height=(args.max + 50) // args.scale,
           nodes=nodes)


def draw_node(node: Node, radius: int = 10, color: tuple = ray.BLACK):
    ray.draw_circle(node.pos_x, node.pos_y, radius, color)


def draw_slider(width, height):
    rect = ray.Rectangle(0, height - 50, width, 50)
    ray.gui_slider(rect, "OI", "TCHAU", 0, 50, 60, 100)


def render(nodes, width, height):
    ray.init_window(width, height, "Vanet Visualizer")

    while not ray.window_should_close():
        ray.begin_drawing()
        ray.clear_background(ray.WHITE)
        ray.draw_text("Hello world", 190, 200, 20, ray.VIOLET)

        for node in nodes:
            draw_node(node)

        draw_slider(width, height)
        ray.end_drawing()

    ray.close_window()
