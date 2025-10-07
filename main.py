from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import numpy as np
import math

Window.size = (400, 700)

class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.function = "x**2"
        self.x_min = -5
        self.x_max = 5
        self.y_min = -5
        self.y_max = 5
        self.auto_scale = True
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
    def update_canvas(self, *args):
        if self.width > 0 and self.height > 0:
            self.draw_graph()
        
    def set_function(self, func_text, x_min, x_max):
        try:
            self.function = self.parse_function(func_text)
            self.x_min = float(x_min)
            self.x_max = float(x_max)
            self.draw_graph()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def parse_function(self, text):
        text = text.strip()
        text = text.replace('^', '**')
        text = text.replace('sqrt', 'math.sqrt')
        text = text.replace('ln', 'math.log')
        text = text.replace('log', 'math.log10')
        text = text.replace('e^x', 'math.exp(x)')
        text = text.replace('π', 'math.pi')
        text = text.replace('pi', 'math.pi')
        
        # Добавляем умножение там, где оно подразумевается
        import re
        text = re.sub(r'(\d)([a-df-z\(])', r'\1*\2', text)  # число перед переменной/функцией
        text = re.sub(r'(\))(\d|[a-df-z\(])', r'\1*\2', text)  # скобка перед числом/переменной
        text = re.sub(r'([a-df-z])(\()', r'\1*\2', text)  # переменная перед скобкой
        
        return text
        
    def calculate_function(self, x):
        try:
            safe_dict = {
                'math': math,
                'np': np,
                'sin': math.sin,
                'cos': math.cos, 
                'tan': math.tan,
                'sqrt': math.sqrt,
                'log': math.log,
                'log10': math.log10,
                'exp': math.exp,
                'abs': abs,
                'x': x
            }
            return eval(self.function, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            return float('nan')
    
    def calculate_y_range(self, num_points=200):
        """Вычисляет автоматический диапазон Y"""
        y_values = []
        for i in range(num_points):
            x_value = self.x_min + (i / (num_points - 1)) * (self.x_max - self.x_min)
            y_value = self.calculate_function(x_value)
            if not math.isnan(y_value) and not math.isinf(y_value):
                y_values.append(y_value)
        
        if not y_values:
            return -1, 1
        
        y_min = min(y_values)
        y_max = max(y_values)
        
        # Добавляем немного места сверху и снизу
        y_range = y_max - y_min
        if y_range < 1e-10:  # Если функция почти постоянная
            y_min -= 1
            y_max += 1
        else:
            padding = y_range * 0.1
            y_min -= padding
            y_max += padding
            
        return y_min, y_max
            
    def draw_graph(self):
        self.canvas.clear()
        
        if self.width == 0 or self.height == 0:
            return
            
        width, height = self.size
        
        with self.canvas:
            # Фон
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # Автоматическое масштабирование Y
            if self.auto_scale:
                self.y_min, self.y_max = self.calculate_y_range()
        
        # Рисуем оси координат
        self.draw_axes(width, height)
        
        # Рисуем сетку
        self.draw_grid(width, height)
        
        # Рисуем график
        self.draw_function(width, height)
    
    def draw_axes(self, width, height):
        with self.canvas:
            Color(0.3, 0.3, 0.3, 1)
            
            # Ось X (если попадает в видимую область)
            if self.y_min <= 0 <= self.y_max:
                y_zero = self.y_to_pixel(0, height)
                Line(points=[self.x, y_zero, self.x + width, y_zero], width=1.5)
            
            # Ось Y (если попадает в видимую область)
            if self.x_min <= 0 <= self.x_max:
                x_zero = self.x_to_pixel(0, width)
                Line(points=[x_zero, self.y, x_zero, self.y + height], width=1.5)
    
    def draw_grid(self, width, height):
        with self.canvas:
            Color(0.9, 0.9, 0.9, 0.5)
            
            # Вертикальные линии сетки
            x_step = self.get_grid_step(self.x_min, self.x_max)
            x = math.ceil(self.x_min / x_step) * x_step
            while x <= self.x_max:
                if abs(x) > 1e-10:  # Не рисуем на оси Y
                    x_pixel = self.x_to_pixel(x, width)
                    Line(points=[x_pixel, self.y, x_pixel, self.y + height], width=0.5)
                x += x_step
            
            # Горизонтальные линии сетки
            y_step = self.get_grid_step(self.y_min, self.y_max)
            y = math.ceil(self.y_min / y_step) * y_step
            while y <= self.y_max:
                if abs(y) > 1e-10:  # Не рисуем на оси X
                    y_pixel = self.y_to_pixel(y, height)
                    Line(points=[self.x, y_pixel, self.x + width, y_pixel], width=0.5)
                y += y_step
    
    def get_grid_step(self, min_val, max_val):
        """Вычисляет оптимальный шаг сетки"""
        range_val = max_val - min_val
        if range_val <= 0:
            return 1
        
        # Выбираем шаг из стандартных значений
        steps = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
        target_steps = 10  # Целевое количество линий сетки
        
        for step in steps:
            if range_val / step <= target_steps * 2:
                return step
        
        return steps[-1]
    
    def x_to_pixel(self, x, width):
        """Преобразует координату X в пиксели"""
        return self.x + (x - self.x_min) / (self.x_max - self.x_min) * width
    
    def y_to_pixel(self, y, height):
        """Преобразует координату Y в пиксели"""
        return self.y + height - (y - self.y_min) / (self.y_max - self.y_min) * height
    
    def draw_function(self, width, height):
        num_points = min(500, int(width * 2))  # Больше точек для гладкости
        
        segments = []  # Список сегментов графика (для обработки разрывов)
        current_segment = []
        
        for i in range(num_points):
            x_value = self.x_min + (i / (num_points - 1)) * (self.x_max - self.x_min)
            y_value = self.calculate_function(x_value)
            
            if not math.isnan(y_value) and not math.isinf(y_value) and self.y_min <= y_value <= self.y_max:
                x_pixel = self.x_to_pixel(x_value, width)
                y_pixel = self.y_to_pixel(y_value, height)
                current_segment.append((x_pixel, y_pixel))
            else:
                if current_segment:  # Завершаем текущий сегмент
                    segments.append(current_segment)
                    current_segment = []
        
        if current_segment:  # Добавляем последний сегмент
            segments.append(current_segment)
        
        # Рисуем все сегменты
        with self.canvas:
            Color(0.2, 0.4, 0.8, 1)
            for segment in segments:
                if len(segment) > 1:
                    points = []
                    for x, y in segment:
                        points.extend([x, y])
                    Line(points=points, width=2.0)

class GraphingApp(App):
    def build(self):
        self.title = "Графики функций"
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # Поле ввода функции
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        input_layout.add_widget(Label(text='y =', size_hint=(0.15, 1), font_size=dp(16)))
        self.function_input = TextInput(
            text='x**2', 
            multiline=False,
            size_hint=(0.85, 1),
            font_size=dp(16),
            background_color=get_color_from_hex('#FFFFFF')
        )
        input_layout.add_widget(self.function_input)
        main_layout.add_widget(input_layout)
        
        # Подсказка
        hint_label = Label(
            text='(sqrt(x), x**2, sin(x), x*(x-5)+7, log(x), tan(x))',
            size_hint=(1, 0.05),
            font_size=dp(12),
            color=get_color_from_hex('#666666')
        )
        main_layout.add_widget(hint_label)
        
        # Диапазон X и кнопка
        range_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        range_layout.add_widget(Label(text='x от:', size_hint=(0.2, 1), font_size=dp(14)))
        self.x_min_input = TextInput(text='-5', multiline=False, size_hint=(0.2, 1), font_size=dp(14))
        range_layout.add_widget(self.x_min_input)
        range_layout.add_widget(Label(text='до:', size_hint=(0.1, 1), font_size=dp(14)))
        self.x_max_input = TextInput(text='5', multiline=False, size_hint=(0.2, 1), font_size=dp(14))
        range_layout.add_widget(self.x_max_input)
        
        self.plot_button = Button(
            text='Построить',
            size_hint=(0.3, 1),
            background_color=get_color_from_hex('#4CAF50'),
            color=get_color_from_hex('#FFFFFF'),
            font_size=dp(14)
        )
        self.plot_button.bind(on_press=self.plot_function)
        range_layout.add_widget(self.plot_button)
        
        main_layout.add_widget(range_layout)
        
        # Примеры функций
        buttons_label = Label(text='Примеры функций:', size_hint=(1, 0.05), font_size=dp(14))
        main_layout.add_widget(buttons_label)
        
        scroll = ScrollView(size_hint=(1, 0.3))
        buttons_layout = GridLayout(cols=3, size_hint_y=None, spacing=dp(5))
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))
        
        examples = [
            'x**2', 'math.sin(x)', 'math.cos(x)', 'math.exp(x)', 
            'math.log(abs(x)+0.1)', 'x**3-3*x', 'math.sqrt(abs(x))', 
            'math.tan(x)', 'x**2+2*x+1', '2*x**2-3*x+1', 
            'x*(x-5)+7', '(x-1)*(x+2)', '1/(x+0.1)', 'abs(x)',
            'math.sin(x)/x', 'math.exp(-x**2)', 'math.log(x+1)'
        ]
        
        display_names = [
            'x²', 'sin(x)', 'cos(x)', 'e^x', 'ln|x|', 'x³-3x', '√|x|', 
            'tan(x)', 'x²+2x+1', '2x²-3x+1', 'x(x-5)+7', '(x-1)(x+2)', 
            '1/x', '|x|', 'sin(x)/x', 'e^(-x²)', 'ln(x+1)'
        ]
        
        for i, example in enumerate(examples):
            btn = Button(
                text=display_names[i],
                size_hint_y=None,
                height=dp(40),
                font_size=dp(12),
                background_color=get_color_from_hex('#2196F3'),
                color=get_color_from_hex('#FFFFFF')
            )
            btn.bind(on_press=lambda instance, ex=example: self.set_example(ex))
            buttons_layout.add_widget(btn)
            
        scroll.add_widget(buttons_layout)
        main_layout.add_widget(scroll)
        
        # График
        self.graph = GraphWidget(size_hint=(1, 0.4))
        main_layout.add_widget(self.graph)
        
        # Статус
        self.status_label = Label(text='Введите функцию и нажмите "Построить"', 
                                 size_hint=(1, 0.05), font_size=dp(12))
        main_layout.add_widget(self.status_label)
        
        # Строим начальный график
        self.plot_function()
        
        return main_layout
    
    def set_example(self, example):
        self.function_input.text = example
        self.plot_function()
        
    def plot_function(self, *args):
        try:
            func_text = self.function_input.text
            x_min = self.x_min_input.text
            x_max = self.x_max_input.text
            
            success = self.graph.set_function(func_text, x_min, x_max)
            if success:
                self.status_label.text = f'График: y = {func_text}'
                self.status_label.color = get_color_from_hex('#388E3C')
            else:
                self.status_label.text = 'Ошибка в функции'
                self.status_label.color = get_color_from_hex('#D32F2F')
            
        except Exception as e:
            self.status_label.text = f'Ошибка: {str(e)}'
            self.status_label.color = get_color_from_hex('#D32F2F')

if __name__ == '__main__':
    GraphingApp().run()