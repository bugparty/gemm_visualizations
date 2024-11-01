
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numba import jit
matplotlib.use('MacOSX')
import time
start_time = time.time()
# Parameters
n = 16  # Matrix size (n x n)
BLOCK_SIZE = 8

# Initialize access matrices to store the access pattern
access_A = np.zeros((n, n))


# Simulate the memory access of dgemm6_kji2 function
def dgemm_kji2_simulation(n, BLOCK_SIZE, tracks):
    for k in range(0, n, BLOCK_SIZE):
        for j in range(0, n, BLOCK_SIZE):
            for i in range(0, n, BLOCK_SIZE):
                for kk in range(k, min(k + BLOCK_SIZE, n)):
                    for jj in range(j, min(j + BLOCK_SIZE, n)):
                        for ii in range(i, min(i + BLOCK_SIZE, n)):
                            # A,B,C 's (x,y) coords
                            tracks.append(((ii, kk),(kk,jj),(ii,jj)))

def dgemm_ikj2_simulation(n, BLOCK_SIZE, tracks):
    for i in range(0, n, BLOCK_SIZE):
        for k in range(0, n, BLOCK_SIZE):
            for j in range(0, n, BLOCK_SIZE):
                for ii in range(i, min(i + BLOCK_SIZE, n)):
                    for kk in range(k, min(k + BLOCK_SIZE, n)):
                        for jj in range(j, min(j + BLOCK_SIZE, n)):
                            tracks.append(((ii, kk),(kk,jj),(ii,jj)))
def dgemm_ijk2_simulation(n, BLOCK_SIZE, tracks):
    for i in range(0, n, BLOCK_SIZE):
            for j in range(0, n, BLOCK_SIZE):
                for k in range(0, n, BLOCK_SIZE):
                    for ii in range(i, min(i + BLOCK_SIZE, n)):
                        for jj in range(j, min(j + BLOCK_SIZE, n)):
                            for kk in range(k, min(k + BLOCK_SIZE, n)):
                                tracks.append(((ii, kk),(kk,jj),(ii,jj)))
                            

# Create an animation of the memory access pattern
fig, ax = plt.subplots(figsize=(6, 5),dpi=900/6)

# Pre-create the grid and matrix plot
matrix = np.zeros((n, n))
cmap = plt.get_cmap('Pastel1')
im = ax.imshow(matrix, cmap=cmap, vmin=-1, vmax=1)

# Draw grid lines only once
for i in range(n + 1):
    ax.axhline(i - 0.5, color='grey', lw=1, alpha=0.7)
    ax.axvline(i - 0.5, color='grey', lw=1, alpha=0.7)

# Set up the axes
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.xaxis.tick_top()
ax.yaxis.tick_left()
ax.set_xticklabels([])
ax.set_yticklabels([])

# Create a rectangle to highlight the current cell
rectR = plt.Rectangle((-0.5, -0.5), 1, 1, linewidth=2, edgecolor='red', facecolor='red', alpha=0.5,label='A')
rectG = plt.Rectangle((-0.5, -0.5), 1, 1, linewidth=2, edgecolor='green', facecolor='green', alpha=0.5,label='B')
rectB = plt.Rectangle((-0.5, -0.5), 1, 1, linewidth=2, edgecolor='blue', facecolor='blue', alpha=0.5, label='C')
rects = [rectR, rectG,rectB]
for rect in rects:
    ax.add_patch(rect)
ax.legend(loc='lower right')

@jit
def update(poses):
    # Update the position of the rectangle instead of redrawing everything
    for rect, posi in zip(rects, poses):
        rect.set_xy((posi[1] - 0.5, posi[0] - 0.5))


FFMPEG_CODEC = 'h264_videotoolbox'
VIDEO_SPEED = 15
frame_interval =  100/VIDEO_SPEED

def draw_kji():
    print("drawing")
    plt.title("kji-kji matrix A,B,C memory access animation")
    ani = animation.FuncAnimation(fig, update,frames=tracks_kji, repeat=False)
    print("saving mp4")
    FFwriter = animation.FFMpegWriter(fps=VIDEO_SPEED,codec=FFMPEG_CODEC)
    ani.save('animation_kji_b{}_spd{}.mp4'.format(BLOCK_SIZE,VIDEO_SPEED), writer = FFwriter)
def draw_ikj():
    print("drawing")
    plt.title("ikj-ikj matrix A,B,C memory access animation")
    ani = animation.FuncAnimation(fig, update,frames=tracks_kji, repeat=False)
    print("saving mp4")
    FFwriter = animation.FFMpegWriter(fps=VIDEO_SPEED,codec=FFMPEG_CODEC)
    ani.save('animation_ikj_b{}_spd{}.mp4'.format(BLOCK_SIZE,VIDEO_SPEED), writer = FFwriter)
def draw_ijk():
    print("drawing")
    plt.title("ijk-ijk matrix A,B,C memory access animation")
    ani = animation.FuncAnimation(fig, update, frames=tracks_ijk, repeat=False)
    print("saving ijk mp4")
    FFwriter = animation.FFMpegWriter(fps=VIDEO_SPEED,codec=FFMPEG_CODEC)
    ani.save('animation_ijk_b{}_spd{}.mp4'.format(BLOCK_SIZE,VIDEO_SPEED), writer = FFwriter)



BLOCK_SIZE=4
# Run the simulation
tracks_kji = []
dgemm_kji2_simulation(n, BLOCK_SIZE, tracks_kji)
draw_kji()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Script execution time: {elapsed_time:.2f} seconds")
start_time = time.time()
tracks_ikj = []
dgemm_ikj2_simulation(n, BLOCK_SIZE, tracks_ikj)
draw_ikj()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Script execution time: {elapsed_time:.2f} seconds")
start_time = time.time()
tracks_ijk = []
dgemm_ijk2_simulation(n, BLOCK_SIZE, tracks_ijk)
draw_ijk()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Script execution time: {elapsed_time:.2f} seconds")
start_time = time.time()