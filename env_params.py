# import pygame

# def setEnvironmentalParameters(parameters_set, running, clock, screen):
#     font = pygame.font.Font(None, 24)
#     box = pygame.Rect(340, 110, 500, 300)
#     pred_box = pygame.Rect(440, 160, 50, 20)
#     temp_box = pygame.Rect(460, 190, 50, 20)
#     fa_box = pygame.Rect(490, 220, 50, 20)
#     pred_box_color = pygame.Color('gray55')
#     temp_box_color = pygame.Color('gray55')
#     fa_box_color = pygame.Color('gray55')
#     pygame.display.flip()
#     white = pygame.Color('white')

#     pred, temp, fa = '', '', ''
#     # this is set to 0, 1, or 2 to indicate which string is "current" respectively
#     curr_str = -1

#     while not parameters_set:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 parameters_set = True
#                 running = False
#                 pygame.quit()
#                 break
#             # check for input box click
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pred_box_color = pygame.Color('gray55')
#                 temp_box_color = pygame.Color('gray55')
#                 fa_box_color = pygame.Color('gray55')
#                 if pred_box.collidepoint(event.pos):
#                     pred_box_color = pygame.Color('grey')
#                     curr_str = 0
#                 elif temp_box.collidepoint(event.pos):
#                     temp_box_color = pygame.Color('grey')
#                     curr_str = 1
#                 elif fa_box.collidepoint(event.pos):
#                     fa_box_color = pygame.Color('grey')
#                     curr_str = 2

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     parameters_set = True
#                     if pred.isdigit() and temp.isdigit() and fa.isdigit():

#                 if event.key == pygame.K_BACKSPACE:
#                     curr_str = curr_str[:-1]
#                 else:
#                     if curr_str == 0:
#                         pred += event.unicode
#                     elif curr_str == 1:
#                         temp += event.unicode
#                     elif curr_str == 2:
#                         fa += event.unicode

#         pygame.draw.rect(screen, pygame.Color('black'), box)
#         pygame.draw.rect(screen, pred_box_color, pred_box)
#         pygame.draw.rect(screen, temp_box_color, temp_box)
#         pygame.draw.rect(screen, fa_box_color, fa_box)
#         static_text_surfs = [
#             font.render("Start by initializing the environmental parameters", True, white),
#             font.render("Predation:", True, white),
#             font.render("Temperature:", True, white),
#             font.render("Food Availability:", True, white)
#         ]
#         screen.blits([
#             (static_text_surfs[0], (370, 120)),
#             (static_text_surfs[1], (350, 160)),
#             (static_text_surfs[2], (350, 190)),
#             (static_text_surfs[3], (350, 220))
#         ])
#         pred_text_surf = font.render(pred, True, white)
#         temp_text_surf = font.render(temp, True, white)
#         fa_text_surf = font.render(fa, True, white)
#         screen.blits([
#             (pred_text_surf, (440, 160)),
#             (temp_text_surf, (460, 190)),
#             (fa_text_surf, (490, 220))
#         ])
#         pygame.display.flip()
#         clock.tick()

