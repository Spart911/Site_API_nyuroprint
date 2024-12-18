import cv2
import os
import numpy as np
import asyncio

async def remove_bg(image_name, in_path="img", out_path="out", main_rect_size=0.02, fg_size=4, resize_to=500):
    img = cv2.imread(os.path.join(in_path, image_name))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_height, img_width = img.shape[:2]
    width, height = img_width, img_height

    # Изменение размера изображения
    if resize_to > 0:
        if img_width > img_height:
            height = resize_to
            width = round(img_width * height / img_height)
        else:
            width = resize_to
            height = round(img_height * width / img_width)

    img_small = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    # Создаем маску
    mask = np.zeros(img_small.shape[:2], np.uint8)

    # Параметры для вырезки фона
    bg_w, bg_h = round(width * main_rect_size), round(height * main_rect_size)
    fg_w, fg_h = round(width * (1 - fg_size) / 2), round(height * (1 - fg_size) / 2)

    bg_rect = (bg_w, bg_h, width - bg_w, height - bg_h)
    fg_rect = (fg_w, fg_h, width - fg_w, height - fg_h)

    # Метки на маске
    cv2.rectangle(mask, fg_rect[:2], fg_rect[2:4], color=1, thickness=-1)

    bgd_model1, fgd_model1 = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)

    # Асинхронное выполнение grabCut
    try:
        await asyncio.to_thread(cv2.grabCut, img_small, mask, bg_rect, bgd_model1, fgd_model1, 3, cv2.GC_INIT_WITH_RECT)
        mask1 = mask.copy()
        cv2.rectangle(mask, (bg_rect[0], bg_rect[1]), (bg_rect[2], bg_rect[3]), color=2, thickness=bg_w * 3)
        await asyncio.to_thread(cv2.grabCut, img_small, mask, bg_rect, bgd_model1, fgd_model1, 10,
                                cv2.GC_INIT_WITH_MASK)
    except Exception:
        mask = mask1.copy()

    mask_result = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')

    # Применяем маску
    masked = cv2.bitwise_and(img_small, img_small, mask=mask_result)
    masked[mask_result < 2] = [0, 0, 255]  # меняем фон на синий

    # Сохраняем результат
    masked = cv2.cvtColor(masked, cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.path.join(out_path, image_name), masked)

async def Dremove_bg(input_path, output_path, image_name, bg_rect_size=0.07, fg_size=0.4, resize=224):
    # Вызываем функцию обработки с передачей аргументов
    await remove_bg(image_name, input_path, output_path, bg_rect_size, fg_size, resize)
