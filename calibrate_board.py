
import cv2

VIDEO_PATH = "video.mp4"  # Change to your sample video path
FRAME_TIME_MS = 2000       # Extract frame at 2 seconds

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise SystemExit(f"Could not open video: {VIDEO_PATH}")

cap.set(cv2.CAP_PROP_POS_MSEC, FRAME_TIME_MS)
ret, frame = cap.read()
cap.release()

if not ret:
    raise SystemExit("Could not read a frame at the selected timestamp.")

height, width = frame.shape[:2]
print(f"Video frame resolution: {width} x {height}")

points = []
display = frame.copy()

def on_click(event, x, y, flags, param):
    if event != cv2.EVENT_LBUTTONDOWN or len(points) >= 4:
        return

    points.append((x, y))
    cv2.circle(display, (x, y), 6, (0, 255, 0), -1)
    cv2.putText(
        display,
        str(len(points)),
        (x + 10, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )
    cv2.imshow("Select chessboard corners", display)
    print(f"Corner {len(points)}: ({x}, {y})")

cv2.namedWindow("Select chessboard corners")
cv2.setMouseCallback("Select chessboard corners", on_click)

print("\nClick the OUTER corners of the chessboard in this order:")
print("1. Top-left")
print("2. Top-right")
print("3. Bottom-right")
print("4. Bottom-left")
print("Press ESC to cancel.\n")

while len(points) < 4:
    cv2.imshow("Select chessboard corners", display)
    key = cv2.waitKey(20) & 0xFF
    if key == 27:
        cv2.destroyAllWindows()
        raise SystemExit("Calibration cancelled.")

cv2.destroyAllWindows()

# Save an annotated frame for reference.
for i in range(4):
    p1 = points[i]
    p2 = points[(i + 1) % 4]
    cv2.line(frame, p1, p2, (0, 255, 0), 2)

cv2.imwrite("calibrated_board.jpg", frame)

print("\nCoordinates in click order:")
print(points)

print("\nLocked corners:")
print(f"        [{points[0][0]:.3f}, {points[0][1]:.3f}],   # TL — outer corner beyond h1")
print(f"        [{points[1][0]:.3f}, {points[1][1]:.3f}],   # TR — outer corner beyond a1")
print(f"        [{points[3][0]:.3f}, {points[3][1]:.3f}],   # BL — outer corner beyond h8")
print(f"        [{points[2][0]:.3f}, {points[2][1]:.3f}],   # BR — outer corner beyond a8")

print("\nAnnotated image saved as calibrated_board.jpg")
