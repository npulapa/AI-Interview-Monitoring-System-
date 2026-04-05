import cv2
import numpy as np
import time
import sys

# ---------------- SETTINGS ----------------
QUESTION_TIME = 30

questions = [
    "Define Object-Oriented Programming and its features.",
    "Explain inheritance with a real-time example.",
    "What is polymorphism and its types?",
    "Compare ArrayList vs LinkedList.",
    "Explain exception handling with try-catch."
]

keywords = {
    0: ["object", "class", "encapsulation", "inheritance", "polymorphism", "abstraction"],
    1: ["inheritance", "parent", "child", "class", "reuse"],
    2: ["polymorphism", "overloading", "overriding", "compile", "runtime"],
    3: ["arraylist", "linkedlist", "access", "insertion", "deletion"],
    4: ["exception", "try", "catch", "error", "runtime"]
}

correct_answers = [
    "OOP is based on objects and includes encapsulation, inheritance, polymorphism, and abstraction.",
    "Inheritance allows a child class to inherit properties from a parent class.",
    "Polymorphism allows methods to behave differently. Types include compile-time and runtime.",
    "ArrayList is faster for access, LinkedList is better for insertion and deletion.",
    "Exception handling uses try and catch blocks to handle runtime errors."
]

answers = []
scores = []

# ---------------- SCORING ----------------
def evaluate_answer(q, ans):
    ans = ans.lower()
    match = sum(1 for word in keywords[q] if word in ans)
    return (match / len(keywords[q])) * 100

# ---------------- FACE DETECTION ----------------
face_model = cv2.dnn.readNetFromCaffe(
    "models/deploy.prototxt",
    "models/res10_300x300_ssd_iter_140000.caffemodel"
)

def detect_face(frame):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    face_model.setInput(blob)
    detections = face_model.forward()

    faces = []
    for i in range(detections.shape[2]):
        if detections[0, 0, i, 2] > 0.6:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            faces.append(box.astype("int"))
    return faces

def is_looking_away(box):
    x1, y1, x2, y2 = box
    return (x2 - x1) / (y2 - y1) < 0.75

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

print("===== AI JAVA INTERVIEW SYSTEM =====")
input("Press ENTER to start interview...\n")

print("\nInterview Started...\n")

# ---------------- MAIN LOOP ----------------
for q_index in range(len(questions)):

    current_answer = ""
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.resize(frame, (1000, 700))

        # ---- FACE ----
        faces = detect_face(frame)
        for (x1, y1, x2, y2) in faces:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

            if is_looking_away((x1, y1, x2, y2)):
                cv2.putText(frame, "LOOKING AWAY", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        # ---- TIMER ----
        elapsed = time.time() - start_time
        remaining = int(QUESTION_TIME - elapsed)

        cv2.putText(frame, f"Time: {remaining}", (850,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        # ---- QUESTION ----
        cv2.putText(frame, questions[q_index], (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        # ---- ANSWER ----
        cv2.putText(frame, "Your Answer:", (20,600),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        cv2.putText(frame, current_answer[-80:], (20,650),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("AI Interview System", frame)

        key = cv2.waitKey(1) & 0xFF

        # ESC → Skip
        if key == 27:
            answers.append("Skipped")
            scores.append(0)
            break

        # Q → Exit
        elif key == ord('q'):
            print("\n❌ Interview Exited by User")
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

        # ENTER → Submit
        elif key == 13:
            break

        # BACKSPACE
        elif key in (8, 127):
            current_answer = current_answer[:-1]

        # SPACE
        elif key == 32:
            current_answer += " "

        # NORMAL CHAR
        elif 32 <= key <= 126:
            current_answer += chr(key)

        # TIME UP
        if remaining <= 0:
            if current_answer.strip() == "":
                answers.append("No Answer")
                scores.append(0)
            else:
                answers.append(current_answer)
                scores.append(evaluate_answer(q_index, current_answer))
            break

    # Store if ENTER pressed
    if len(answers) <= q_index:
        answers.append(current_answer)
        scores.append(evaluate_answer(q_index, current_answer))

    print(f"\nQ{q_index+1}: {questions[q_index]}")
    print("Your Answer:", answers[q_index])
    print(f"✅ Score: {round(scores[q_index], 2)}%")

# ---------------- FINAL REPORT ----------------
cap.release()
cv2.destroyAllWindows()

print("\n========================================")
print("        FINAL INTERVIEW REPORT")
print("========================================\n")

total = 0

for i in range(len(questions)):
    print(f"\nQ{i+1}: {questions[i]}")
    print(f"👉 Your Answer   : {answers[i]}")
    print(f"✔ Correct Answer: {correct_answers[i]}")
    print(f"🔑 Keywords     : {', '.join(keywords[i])}")
    print(f"📊 Score        : {round(scores[i], 2)}%")

    total += scores[i]

avg = total / len(scores)

print("\n----------------------------------------")
print(f"🧠 Overall Score: {round(avg, 2)}%")
print("----------------------------------------")

if avg > 75:
    print("🎉 Excellent Performance!")
elif avg > 50:
    print("👍 Good, but can improve.")
else:
    print("⚠️ Needs Improvement.")

print("\n✅ Interview Completed Successfully!")