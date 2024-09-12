import json
import struct
import numpy as np
from scipy.spatial import Delaunay
import tqdm


ofa_lip_map = {
    "A":(0.8,0.2),
    "a":(0.2,0.1),
    "I":(0.24,0.0),
    "O":(0.6,0.8),
    "E":(0.5,0.0),
    "U":(0.3,0.9)
}

def cvt_float(d):
    return struct.unpack('>f',d)[0]
def is_valid(f):
    if f<0 or f>1:
        return False
    return True

def point_in_triangle(p,a,b,c):
    def sign(p1,p2,p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    d1,d2,d3 = sign(p,a,b),sign(p,b,c),sign(p,c,a)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def barycentric_coordinates(triangle, point):
    # triangle是一个包含三个顶点坐标的列表，point是待计算的点坐标
    A, B, C = triangle
    P = np.array(point)
    
    # 计算三角形的面积
    triangle_area = 0.5 * np.linalg.norm(np.cross(B - A, C - A))
    
    # 计算点P相对于三角形ABC各个顶点的面积比例（重心坐标）
    alpha = 0.5 * np.linalg.norm(np.cross(B - P, C - P)) / triangle_area
    beta = 0.5 * np.linalg.norm(np.cross(C - P, A - P)) / triangle_area
    gamma = 1.0 - alpha - beta
    
    return alpha, beta, gamma

def parse_ofa(ofa_file):
    animation_points = np.array([(0, 1),(1, 0),(1, 1),(0, 0),*ofa_lip_map.values()])
    tri = Delaunay(animation_points)

    with open(ofa_file,'rb') as f:
        data = f.read()
    positions = []
    for ind,i in enumerate(range(len(data)-12,-1,-12)):
        block = data[i:i+12]
        if len(block)!=12:
            break
        a,b,c = data[i:i+4],data[i+4:i+8],data[i+8:i+12]
        a,b,c = map(cvt_float,(a,b,c))
        if all(map(is_valid,(a,c))):
                positions.append((a,c))
        else:
            break
    
    weights = []
    for point in tqdm.tqdm(positions[::-1]):
        for simplex in tri.simplices:
            vertices = animation_points[simplex]
            if point_in_triangle(point,*vertices):
                weight = barycentric_coordinates(vertices,point)
                weight = list(weight)
                for i in range(3):
                    if simplex[i] <3:
                        weight[i]=0
                weight = np.array(weight)
                weight = weight*np.sum(weight)
                weight = weight.clip(0,1)
                simplex
                v = [0]*len(animation_points)
                for ind,s in enumerate(simplex):
                    v[s] = weight[ind]
                weights.append(v[3:])
                break
    return weights
                
                

