import cv2
import numpy as np

def inputstring(rect_start, rect_end, text_x, text_y, text):
    exit_input = 0
    # 创建一个黑色背景的图像
    frame = np.zeros((500, 500, 3), np.uint8)

    # 定义一个字符串
    str_input = ""

    # 定义光标状态
    cursor_visible = True

    # 定义一个标志，表示是否开始输入
    start_input = False

    # 定义一个标志，表示光标是否闪烁
    cursor_blinking = False

    # 定义回调函数，用于处理鼠标点击事件
    def mouse_callback(event, x, y, flags, param):
        nonlocal start_input, cursor_blinking
        if event == cv2.EVENT_LBUTTONDOWN:
            if rect_start[0] <= x <= rect_end[0] and rect_start[1] <= y <= rect_end[1]:
                start_input = True
                cursor_blinking = True  # 开始光标闪烁
            else:
                start_input = False
                cursor_blinking = False  # 停止光标闪烁

    # 定义回调函数，用于处理键盘输入事件
    def on_key(event):
        nonlocal str_input, start_input, exit_input
        if start_input:
            if event == 13:  # Enter key
                print(f"User input: {str_input}")
                str_input = ""
                exit_input = 1
            elif event == 8:  # Backspace key
                str_input = str_input[:-1]
            else:
                str_input += chr(event)
            update_frame()

    def update_frame():
        nonlocal str_input, cursor_visible, rect_start, rect_end
        # 在图像上显示用户输入的字符串和光标
        frame[:] = 0  # 清除之前的内容
        cv2.rectangle(frame, rect_start, rect_end, (255, 255, 255), 2)
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        display_text = str_input + ("_" if cursor_visible else "")
        cv2.putText(frame, display_text, (rect_start[0] + 10, rect_start[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Image with Subtitle', frame)

    def toggle_cursor():
        nonlocal cursor_visible
        cursor_visible = not cursor_visible
        update_frame()

    # 设置鼠标回调函数
    cv2.namedWindow('Image with Subtitle')
    cv2.setMouseCallback('Image with Subtitle', mouse_callback)

    # 显示初始图像
    update_frame()

    # 启动光标闪烁
    while True:
        if cursor_blinking:
            toggle_cursor()
        key = cv2.waitKey(500)  # 每500毫秒切换一次光标状态
        if key != -1:
            on_key(key)
        if key == 27:  # ESC键退出
            return str_input
        if exit_input == 1:
            return str_input

#inputstring((100, 100), (400, 200), 100, 100, "HelloWorld")


# class inputstring:
#     def __init__(self,rect_start, rect_end, text_x, text_y, text):
#         self.rect_start=rect_start
#         self.rect_end=rect_end
#         self.text_x=text_x
#         self.text_y=text_y
#         self.text=text

#     def inputstring(rect_start, rect_end, text_x, text_y, text):
#         exit_input = 0
#         # 创建一个黑色背景的图像
#         frame = np.zeros((500, 500, 3), np.uint8)

#         # 定义一个字符串
#         str_input = ""

#         # 定义光标状态
#         cursor_visible = True

#         # 定义一个标志，表示是否开始输入
#         start_input = False

#         # 定义一个标志，表示光标是否闪烁
#         cursor_blinking = False

#         # 定义回调函数，用于处理鼠标点击事件
#         def mouse_callback(event, x, y, flags, param):
#             nonlocal start_input, cursor_blinking
#             if event == cv2.EVENT_LBUTTONDOWN:
#                 if rect_start[0] <= x <= rect_end[0] and rect_start[1] <= y <= rect_end[1]:
#                     start_input = True
#                     cursor_blinking = True  # 开始光标闪烁
#                 else:
#                     start_input = False
#                     cursor_blinking = False  # 停止光标闪烁

#         # 定义回调函数，用于处理键盘输入事件
#         def on_key(event):
#             nonlocal str_input, start_input, exit_input
#             if start_input:
#                 if event == 13:  # Enter key
#                     print(f"User input: {str_input}")
#                     str_input = ""
#                     exit_input = 1
#                 elif event == 8:  # Backspace key
#                     str_input = str_input[:-1]
#                 else:
#                     str_input += chr(event)
#                 update_frame()

#         def update_frame():
#             nonlocal str_input, cursor_visible, rect_start, rect_end
#             # 在图像上显示用户输入的字符串和光标
#             frame[:] = 0  # 清除之前的内容
#             cv2.rectangle(frame, rect_start, rect_end, (255, 255, 255), 2)
#             (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

#             cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

#             display_text = str_input + ("_" if cursor_visible else "")
#             cv2.putText(frame, display_text, (rect_start[0] + 10, rect_start[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
#             cv2.imshow('Image with Subtitle', frame)

#         def toggle_cursor():
#             nonlocal cursor_visible
#             cursor_visible = not cursor_visible
#             update_frame()

#         # 设置鼠标回调函数
#         cv2.namedWindow('Image with Subtitle')
#         cv2.setMouseCallback('Image with Subtitle', mouse_callback)

#         # 显示初始图像
#         update_frame()

#         # 启动光标闪烁
#         while True:
#             if cursor_blinking:
#                 toggle_cursor()
#             key = cv2.waitKey(500)  # 每500毫秒切换一次光标状态
#             if key != -1:
#                 on_key(key)
#             if key == 27:  # ESC键退出
#                 return str_input
#             if exit_input == 1:
#                 return str_input

#     # 调用 input 函数
#     inputstring((100, 100), (400, 200), 100, 100, "HelloWorld")