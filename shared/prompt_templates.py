# Shared prompt templates for AI models

LESSON_PLAN_TEMPLATE = """
Create a comprehensive lesson plan for a multi-grade classroom in rural India with the following specifications:

**Classroom Context:**
- Subject: {subject}
- Topic: {topic}
- Grade Levels: {grades}
- Duration: {duration} minutes
- Student Count: {student_count}
- Learning Objectives: {objectives}
- Available Resources: {resources}

**Requirements:**
- Differentiated activities for each grade level
- Minimal resource requirements suitable for rural schools
- Interactive and engaging methods
- Assessment strategies
- Adaptations for different learning abilities
- Clear instructions for the teacher

**Format the response with these sections:**
1. **Learning Objectives** (by grade level)
2. **Materials Needed** (locally available items preferred)
3. **Lesson Structure**
   - Introduction (5-10 minutes)
   - Main Activity (varies by duration)
   - Conclusion (5-10 minutes)
4. **Grade-Specific Activities**
5. **Assessment Methods**
6. **Extension Activities/Homework**
7. **Teaching Tips & Adaptations**

Make it practical, culturally relevant, and achievable with limited resources.
"""

WORKSHEET_TEMPLATE = """
Create a worksheet for {subject} on the topic "{topic}" for Grade {grade} students in rural India.

**Worksheet Requirements:**
- Age-appropriate questions for Grade {grade}
- Mix of question types: multiple choice, short answer, and problem-solving
- Clear instructions in simple language
- 8-12 questions total
- Difficulty progression from easy to challenging
- Visual elements where possible (simple drawings/diagrams)
- Answer key included
- Cultural context relevant to rural Indian students

**Format:**
1. Header with subject, topic, grade, and student name field
2. Clear instructions
3. Questions organized by difficulty
4. Space for answers
5. Separate answer key

Make it printable in black and white and suitable for photocopying.
"""

VISUAL_AID_TEMPLATE = """
Suggest visual aids and teaching materials for the topic "{topic}" in {subject} for Grade {grade} students.

**Consider:**
- Limited budget and resources in rural schools
- Locally available materials
- Simple tools and supplies
- Reusable materials
- Student participation in creation

**Provide suggestions for:**
1. **Charts and Posters** (hand-drawn or printed)
2. **3D Models** (using clay, cardboard, natural materials)
3. **Interactive Materials** (flashcards, games, manipulatives)
4. **Demonstration Tools** (simple experiments, props)
5. **Student Projects** (group activities, presentations)

**For each suggestion include:**
- Materials needed
- Step-by-step creation instructions
- How to use in the lesson
- Cost estimate (if any)
- Alternative options

Focus on creativity and local resource utilization.
"""

ASSESSMENT_TEMPLATE = """
Create a comprehensive assessment for {subject} - "{topic}" for Grade {grade} students.

**Assessment Components:**
1. **Formative Assessment** (during lesson)
   - Quick check questions
   - Observation checklist
   - Exit ticket questions

2. **Summative Assessment** (end of unit)
   - Multiple choice questions (5)
   - Short answer questions (3-4)
   - Problem-solving questions (2-3)
   - One essay/extended response question

3. **Practical Assessment** (hands-on)
   - Demonstration tasks
   - Project-based evaluation
   - Peer assessment activities

4. **Rubric for Grading**
   - Clear criteria for each level
   - Points allocation
   - Feedback guidelines

**Make it:**
- Aligned with learning objectives
- Appropriate for the grade level
- Culturally sensitive
- Easy to administer with limited resources
- Includes accommodations for different learning needs
"""

STORY_TEMPLATE = """
Create an engaging educational story for Grade {grade} students that teaches the concept of "{topic}" in {subject}.

**Story Requirements:**
- Appropriate length for Grade {grade} (200-500 words)
- Indian cultural context and characters
- Rural setting that students can relate to
- Clear educational objective woven into the narrative
- Simple language and vocabulary
- Engaging plot with relatable characters
- Moral or lesson that reinforces the learning objective

**Include:**
1. **Story Title**
2. **Main Characters** (with brief descriptions)
3. **Setting** (rural Indian context)
4. **Plot** (beginning, middle, end)
5. **Educational Content** (naturally integrated)
6. **Discussion Questions** (3-5 questions to reinforce learning)
7. **Extension Activities** (related to the story)

Make it culturally appropriate and inspiring for rural students.
"""

# Common constants for Indian education context
INDIAN_SUBJECTS = [
    "Mathematics",
    "Science", 
    "English",
    "Hindi",
    "Social Studies",
    "Environmental Studies (EVS)",
    "Art and Craft",
    "Physical Education",
    "Computer Science",
    "Moral Science"
]

GRADE_LEVELS = list(range(1, 13))  # Grades 1-12

COMMON_RESOURCES = [
    "Blackboard and chalk",
    "Chart paper",
    "Colored pencils/crayons",
    "Scissors and glue",
    "Cardboard/old boxes",
    "Natural materials (stones, leaves, sticks)",
    "Old newspapers/magazines",
    "Clay or playdough",
    "Measuring tools (ruler, scale)",
    "Basic stationery"
]

LEARNING_STYLES = [
    "Visual learners",
    "Auditory learners", 
    "Kinesthetic learners",
    "Reading/writing learners"
]

ASSESSMENT_TYPES = [
    "Formative assessment",
    "Summative assessment",
    "Peer assessment",
    "Self-assessment",
    "Portfolio assessment",
    "Performance-based assessment"
]
