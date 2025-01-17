import pygame, math, sys
import numpy as np

pygame.init()
display_scale = (640, 480)
display_center = (display_scale[0] / 2, display_scale[1] / 2)
window = pygame.display.set_mode(display_scale)

depth_buffer = np.full(display_scale, float('inf'))

def calculateVector(p1, p2) -> tuple:
    return (p2[0] - p1[0], p2[1] - p1[1])

def magnitude(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)

def dist3D(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def renderMesh(mesh):
    screenSpaceMesh = []
    for tri in mesh:
        triMesh = [None, None, None, tri[3], None, None]
        ptIdx = 0
        vertices = tri[:3]

        for point in tri[:3]:
            screenSpacePosition = (point[0], point[1])
            screenSpaceVector = calculateVector(point, display_center)
            screenSpaceVector = (screenSpaceVector[0] / magnitude(screenSpaceVector), screenSpaceVector[1] / magnitude(screenSpaceVector))
            screenSpacePosition = (screenSpacePosition[0] + screenSpaceVector[0] * point[2] / 4, screenSpacePosition[1] + screenSpaceVector[1] * point[2] / 4)
            
            triMesh[ptIdx] = screenSpacePosition
            ptIdx += 1

        center = (sum(p[0] for p in tri[:3]) / 3, sum(p[1] for p in tri[:3]) / 3, sum(p[2] for p in tri[:3]) / 3)
        depth = dist3D(center, (display_center[0], display_center[1], 0))

        triMesh[4] = depth

        screenSpaceMesh.append(triMesh)

    screenSpaceMesh = sorted(screenSpaceMesh, key=lambda x: x[4], reverse=True)

    for tri in screenSpaceMesh:
        vertices = []
        for x in range(3):
            vertices.append(tri[x])

        pygame.draw.polygon(window, tri[3], vertices)

    pygame.draw.circle(window, (255, 255, 255), (display_center[0], display_center[1]), 5)

def rotatePoint(point, origin, rotation):

    xRot = math.radians(rotation[0])
    originVector = calculateVector((origin[2], origin[1]), (point[2], point[1]))
    xRot += math.atan2(originVector[1], originVector[0])
    point = (
        point[0],
        origin[1] + math.sin(xRot) * magnitude(originVector), 
        origin[2] + math.cos(xRot) * magnitude(originVector)
    )

    
    yRot = math.radians(rotation[1])
    originVector = calculateVector((origin[0], origin[2]), (point[0], point[2]))
    yRot += math.atan2(originVector[1], originVector[0])
    point = (
        origin[0] + math.cos(yRot) * magnitude(originVector), 
        point[1],
        origin[2] + math.sin(yRot) * magnitude(originVector)
    )

    zRot = math.radians(rotation[2])
    originVector = calculateVector((origin[0], origin[1]), (point[0], point[1]))
    zRot += math.atan2(originVector[1], originVector[0])
    point = (
        origin[0] + math.cos(zRot) * magnitude(originVector), 
        origin[1] + math.sin(zRot) * magnitude(originVector), 
        point[2]
    )

    return point

object_rotation = (0, 0, 0)

font = pygame.font.Font(None, 25)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    object_origin = (display_center[0], display_center[1], 100)

    mesh = [
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 0, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 0, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 0, object_rotation[2])),
            (0, 0, 255)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 0, object_rotation[2])),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 0, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 0, object_rotation[2])),
            (0, 0, 255)
        ),


        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 180, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 180, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 180, object_rotation[2])),
            (0, 0, 255)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 180, object_rotation[2])),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 180, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 180, object_rotation[2])),
            (0, 0, 255)
        ),


        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 90, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 90, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 90, object_rotation[2])),
            (255, 0, 0)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 90, object_rotation[2])),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 90, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 90, object_rotation[2])),
            (255, 0, 0)
        ),

        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 270, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 270, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 270, object_rotation[2])),
            (255, 0, 0)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 270, object_rotation[2])),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 270, object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0], object_rotation[1] + 270, object_rotation[2])),
            (255, 0, 0)
        ),


        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0] + 90, object_rotation[1], object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, (object_rotation[0] + 90, object_rotation[1], object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0] + 90, object_rotation[1], object_rotation[2])),
            (0, 255, 0)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0] + 90, object_rotation[1], object_rotation[2])),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, (object_rotation[0] + 90, object_rotation[1], object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0] + 90, object_rotation[1], object_rotation[2])),
            (0, 255, 0)
        ),


        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0] + 270, object_rotation[1], object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, (object_rotation[0] + 270, object_rotation[1], object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0] + 270, object_rotation[1], object_rotation[2])),
            (0, 255, 0)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, (object_rotation[0] + 270, object_rotation[1], object_rotation[2])),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, (object_rotation[0] + 270, object_rotation[1], object_rotation[2])),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, (object_rotation[0] + 270, object_rotation[1], object_rotation[2])),
            (0, 255, 0)
        ),
    ]

    mx, my = pygame.mouse.get_pos()

    if pygame.key.get_pressed()[pygame.K_d]:
        object_rotation = (object_rotation[0], object_rotation[1] + 0.05, object_rotation[2])
    if pygame.key.get_pressed()[pygame.K_a]:
        object_rotation = (object_rotation[0], object_rotation[1] - 0.05, object_rotation[2])

    if pygame.key.get_pressed()[pygame.K_w]:
        object_rotation = (object_rotation[0] + 0.05, object_rotation[1], object_rotation[2])
    if pygame.key.get_pressed()[pygame.K_s]:
        object_rotation = (object_rotation[0] - 0.05, object_rotation[1], object_rotation[2])

    

    window.fill((0, 0, 0))

    renderMesh(mesh)

    fpsText = font.render(str(int(clock.get_fps())), True, (255, 255, 255))

    window.blit(fpsText, (0,0))

    pygame.display.flip()
    depth_buffer.fill(float('inf'))

    clock.tick()