import pygame, math, sys
import numpy as np


display_scale = (640, 480)
display_center = (display_scale[0] / 2, display_scale[1] / 2)
window = pygame.display.set_mode(display_scale)

depth_buffer = np.full(display_scale, float('inf'))

def calculateVector(p1, p2) -> tuple:
    return (p2[0] - p1[0], p2[1] - p1[1])

def magnitude(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)

def dist3D(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)

def renderMesh(mesh):
    screenSpaceMesh = []
    lowestDist = float('inf')
    for tri in mesh:
        triMesh = [None, None, None, tri[3]]
        ptIdx = 0
        vertices = []
        for x in range(3):
            vertices.append(tri[x])

        for point in vertices:
            screenSpacePosition = (point[0], point[1])
            screenSpaceVector = calculateVector(point, display_center)
            screenSpaceVector = (screenSpaceVector[0] / magnitude(screenSpaceVector), screenSpaceVector[1] / magnitude(screenSpaceVector))
            screenSpacePosition = (screenSpacePosition[0] + screenSpaceVector[0] * point[2] / 4, screenSpacePosition[1] + screenSpaceVector[1] * point[2] / 4)
            

            pygame.draw.circle(window, (255, 0, 0), screenSpacePosition, 2)
            triMesh[ptIdx] = screenSpacePosition
            ptIdx += 1

        center = (sum(p[0] for p in triMesh) / 3, sum(p[1] for p in triMesh) / 3, sum(p[2] for p in tri) / 3)
        depth = dist3D(center, (display_center[0], display_center[1], 0))

        if depth < lowestDist:
            screenSpaceMesh.append(triMesh)
            lowestDist = depth
        else:
            print("Inserting")
            screenSpaceMesh.insert(0, triMesh)

    for tri in screenSpaceMesh:
        vertices = []
        for x in range(3):
            vertices.append(tri[x])

        pygame.draw.polygon(window, tri[3], vertices)

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    object_origin = (display_center[0], display_center[1], 100)

    mesh = [
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, object_rotation),
            (0, 0, 255)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, object_rotation),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, object_rotation),
            (0, 0, 255)
        ),

        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 200), object_origin, object_rotation),
            (0, 0, 255)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 200), object_origin, object_rotation),
            (0, 0, 255)
        ),


        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 1), object_origin, object_rotation),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, object_rotation),
            (255, 0, 0)
        ),
        (
            rotatePoint((display_center[0] - 100, display_center[1] - 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] - 100, display_center[1] + 100, 1), object_origin, object_rotation),
            (255, 0, 0)
        ),

        (
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 1), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, object_rotation),
            (255, 0, 0)
        ),
        (
            rotatePoint((display_center[0] + 100, display_center[1] + 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 200), object_origin, object_rotation),
            rotatePoint((display_center[0] + 100, display_center[1] - 100, 1), object_origin, object_rotation),
            (255, 0, 0)
        ),
        

        
    ]

    object_rotation = (object_rotation[0], object_rotation[1] + 0.07, object_rotation[2])

    

    window.fill((0, 0, 0))

    renderMesh(mesh)

    pygame.display.flip()
    depth_buffer.fill(float('inf'))