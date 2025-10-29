"""
Fitness Knowledge Base - Enhanced context for better AI responses
No training needed - just better prompts with expert knowledge!
"""

# Progressive Overload Principles
PROGRESSIVE_OVERLOAD = """
PROGRESSIVE OVERLOAD PRINCIPLES:
- Linear Progression: Add 2.5-5lbs when you complete all sets at target reps for 2 consecutive workouts
- Double Progression: Increase reps first (8-12 range), then add weight when you hit top of range
- Wave Loading: Alternate heavy (3-5 reps), medium (6-8), light (10-12) across workouts
- Deload Protocol: Every 4-6 weeks, reduce volume by 40% or intensity by 10% for recovery

READINESS TO INCREASE WEIGHT:
- Sleep >7.5hrs + Soreness <4/10 + Recent lifts felt smooth = Add 2.5-5lbs
- Sleep 6-7hrs + Soreness 4-6/10 + Bar moved well = Maintain weight, increase reps
- Sleep <6hrs OR Soreness >7/10 = Reduce volume 20% or take rest day

PR ATTEMPT GUIDELINES:
- Only attempt when recovery score >85% (sleep + soreness + energy)
- Single attempts: Add 5-10lbs to current max
- Rep PRs: Keep weight, try for +1-2 reps
- Rest 3-5 minutes between max attempts
"""

# Exercise-Specific Knowledge
EXERCISES = {
    "bench_press": """
BENCH PRESS:
Primary: Chest (pectoralis major)
Secondary: Triceps, anterior deltoids

FORM CUES:
- Retract and depress scapula (pull shoulder blades down and back)
- Maintain arch in lower back
- Feet flat on floor, drive through heels
- Bar path: Straight down to nipple line, press up and slightly back
- Elbows: 45-degree angle from torso (not flared to 90 degrees)
- Grip: Slightly wider than shoulder width
- Lower to touch chest, press explosively

PROGRESSION:
- Beginner (<135lbs): Add 5lbs every session
- Intermediate (135-225lbs): Add 2.5lbs every 1-2 sessions
- Advanced (225+): Wave loading, add weight every 2-3 weeks

ASSISTANCE EXERCISES:
- Close-grip bench (triceps)
- Incline press (upper chest)
- Dips (overall pressing strength)
- Face pulls (shoulder health)

COMMON ISSUES:
- Bouncing bar off chest → Control descent, pause
- Elbows flaring → Keep at 45 degrees
- Butt lifting off bench → Engage core, maintain arch
- Uneven press → Check grip width, practice with pause reps
""",

    "squat": """
SQUAT:
Primary: Quadriceps, glutes
Secondary: Hamstrings, core, adductors

FORM CUES:
- Bar position: High bar (traps) or low bar (rear delts)
- Stance: Shoulder-width or slightly wider
- Toes: Slightly pointed out (10-30 degrees)
- Depth: Hip crease below knee (parallel or deeper)
- Knees: Track over toes, don't cave inward
- Chest: Up and proud throughout
- Core: Brace hard, valsalva maneuver
- Bar path: Straight vertical line over mid-foot

PROGRESSION:
- Beginner (<185lbs): Add 5-10lbs every session
- Intermediate (185-315lbs): Add 5lbs every 1-2 sessions
- Advanced (315+): Wave loading, weekly progression

ASSISTANCE EXERCISES:
- Front squats (quad emphasis, core)
- Bulgarian split squats (unilateral)
- Leg press (volume without CNS fatigue)
- Pause squats (strength out of hole)

COMMON ISSUES:
- Knees caving (valgus) → Cue "knees out", strengthen glutes
- Forward lean → Work on ankle mobility, try high bar
- Not hitting depth → Goblet squats for mobility, box squats
- Butt wink → Improve hip mobility, adjust stance width
""",

    "deadlift": """
DEADLIFT:
Primary: Erectors, glutes, hamstrings
Secondary: Lats, traps, grip, core

FORM CUES:
- Stance: Hip-width, toes under bar
- Grip: Just outside legs, mixed or double overhand
- Setup: Bar over mid-foot, shins touch bar
- Back: Neutral spine, chest up
- Hinge: Push hips back, maintain back angle until bar passes knees
- Drive: Push floor away, hips and shoulders rise together
- Lockout: Stand tall, squeeze glutes

PROGRESSION:
- Beginner (<225lbs): Add 10lbs every session
- Intermediate (225-405lbs): Add 5-10lbs every session
- Advanced (405+): Weekly progression, consider sumo variant

ASSISTANCE EXERCISES:
- Romanian deadlifts (hamstrings)
- Deficit deadlifts (off the floor strength)
- Rack pulls (lockout strength)
- Barbell rows (back thickness)

COMMON ISSUES:
- Rounded back → Reduce weight, cue "chest up"
- Bar drifting away → Keep bar close, engage lats
- Weak lockout → Rack pulls, hip thrusts
- Weak off floor → Deficit deadlifts, pause deadlifts
""",

    "overhead_press": """
OVERHEAD PRESS (OHP):
Primary: Anterior deltoids, triceps
Secondary: Upper chest, core, traps

FORM CUES:
- Stance: Hip-width, slight stagger optional
- Grip: Just outside shoulders
- Starting position: Clavicles, elbows slightly forward
- Press: Straight overhead, push head through at top
- Lockout: Shrug shoulders up, full extension
- Core: Brace hard, squeeze glutes (prevent arch)

PROGRESSION:
- Beginner (<95lbs): Add 2.5lbs every session
- Intermediate (95-135lbs): Add 2.5lbs every 1-2 sessions
- Advanced (135+): Use microplates (1.25lbs), weekly progression

ASSISTANCE EXERCISES:
- Push press (overload lockout)
- Seated DB press (isolate shoulders)
- Lateral raises (side delts)
- Face pulls (rear delts, shoulder health)

COMMON ISSUES:
- Excessive back arch → Brace core harder, squeeze glutes
- Bar drifts forward → Press back into shrug
- Stalling → Most sensitive to fatigue, ensure recovery
- Elbow pain → Check grip width, add face pulls
"""
}

# Recovery and Nutrition
RECOVERY_NUTRITION = """
RECOVERY INDICATORS:
Sleep Quality:
- 8+ hours = Optimal recovery, ready for heavy training
- 7-7.5 hours = Good, can handle normal training
- 6-7 hours = Suboptimal, reduce volume 10-20%
- <6 hours = Poor, consider rest day or light technique work

Soreness (DOMS):
- 1-3/10 = Minimal, fully recovered, can increase intensity
- 4-6/10 = Moderate, maintain or slightly reduce volume
- 7-8/10 = High, reduce volume 30%, focus on mobility
- 9-10/10 = Severe, rest day or active recovery only

Energy Levels:
- High = CNS recovered, good for PRs and heavy training
- Moderate = Normal training, avoid max attempts
- Low = Overreaching possible, reduce intensity or rest

RECOVERY SCORE CALCULATION:
Score = (Sleep/8 × 40) + ((10-Soreness) × 30) + (Energy × 30)
- 85-100% = Optimal, attempt PRs
- 70-84% = Good, normal training
- 50-69% = Compromised, reduce volume
- <50% = Poor, rest or active recovery

NUTRITION TARGETS:
Protein:
- Muscle gain: 0.8-1g per lb bodyweight
- Fat loss: 1-1.2g per lb bodyweight
- Timing: Spread across 4-5 meals, 25-40g per meal

Calories:
- Muscle gain: +300-500 above maintenance
- Fat loss: -300-500 below maintenance
- Maintenance: Bodyweight × 14-16

Hydration:
- Base: Bodyweight (lbs) ÷ 2 = oz per day
- Training day: Add 16-24oz
- Signs of dehydration: Dark urine, decreased performance

Pre-Workout:
- 2-3 hours before: Mixed meal (protein + carbs)
- 30-60 min before: Light carbs (banana, rice cake)
- Caffeine: 3-6mg per kg bodyweight if tolerated

Post-Workout:
- Within 2 hours: 20-40g protein + carbs
- Carbs: 0.5-1g per kg bodyweight
- Focus on whole foods: chicken, rice, vegetables
"""

# Training Programs
PROGRAMS = """
BEGINNER PROGRAMS (0-6 months training):

Starting Strength / StrongLifts 5×5:
- 3 days/week, alternating A/B workouts
- Workout A: Squat 5×5, Bench 5×5, Row 5×5
- Workout B: Squat 5×5, OHP 5×5, Deadlift 1×5
- Add 5lbs lower body, 2.5lbs upper body each session

INTERMEDIATE PROGRAMS (6-24 months):

Texas Method:
- Monday (Volume): Squat 5×5, Bench 5×5, Deadlift 5×5
- Wednesday (Light): Squat 2×5 @80%, OHP 3×5, Chin-ups
- Friday (Intensity): Squat 1×5 (PR), Bench 1×5 (PR), Row 3×5

5/3/1:
- 4-week waves: 65%×5, 75%×5, 85%×5+ (Week 1)
- Add 5lbs upper, 10lbs lower each cycle
- Assistance: 50-100 reps push/pull/legs

ADVANCED PROGRAMS (2+ years):

Conjugate Method:
- Max Effort day (work up to 1-3RM)
- Dynamic Effort day (speed work 50-60%)
- Repetition day (volume 8-12 reps)
- Rotate exercises every 1-3 weeks

Block Periodization:
- Accumulation: 4 weeks, high volume (65-75%)
- Intensification: 3 weeks, moderate volume (75-85%)
- Realization: 2 weeks, low volume (85-95%)
- Deload: 1 week, active recovery
"""

# Injury Prevention
INJURY_PREVENTION = """
COMMON INJURIES & PREVENTION:

Lower Back Pain:
- Causes: Rounded back deadlifts, excessive arch in squat
- Prevention: Core work (planks, ab wheel), neutral spine
- Rehab: Bird dogs, dead bugs, McGill big 3

Shoulder Impingement:
- Causes: Poor bench form, overhead pressing imbalances
- Prevention: Face pulls 100+ reps/week, external rotations
- Rehab: Band pull-aparts, YTWs, reduce pressing volume

Knee Pain:
- Causes: Valgus collapse, poor squat depth, overuse
- Prevention: Glute strengthening, proper warm-up
- Rehab: Terminal knee extensions, reverse nordics, reduce volume

Elbow Tendinitis:
- Causes: High-volume pressing/pulling, poor grip
- Prevention: Vary grips, don't lock out fully on every rep
- Rehab: Eccentric wrist curls, reduce volume, ice

RED FLAGS (Stop immediately):
- Sharp pain (not muscle soreness)
- Joint pain that worsens with movement
- Numbness or tingling
- Pain that persists >1 week
- Seek medical professional if any of these occur

WARM-UP PROTOCOL:
1. General: 5-10min cardio (bike, row, jump rope)
2. Dynamic: Leg swings, arm circles, bodyweight squats
3. Specific: Empty bar → 50% → 70% → 85% → Working weight
4. Mobility: Focus on tight areas (hips, shoulders, ankles)
"""

def get_relevant_knowledge(user_query, user_data=None):
    """
    Retrieve relevant knowledge based on user query and data
    This is like RAG (Retrieval Augmented Generation)
    """
    knowledge_chunks = []

    # Always include progressive overload
    knowledge_chunks.append(PROGRESSIVE_OVERLOAD)

    # Check which exercises are mentioned
    query_lower = user_query.lower()
    for exercise, info in EXERCISES.items():
        if exercise.replace("_", " ") in query_lower:
            knowledge_chunks.append(info)

    # Include recovery if relevant
    if user_data:
        if user_data.get('sleep_hours') or user_data.get('soreness'):
            knowledge_chunks.append(RECOVERY_NUTRITION)

    # Check for program-related queries
    if any(word in query_lower for word in ['program', 'routine', 'plan', 'schedule']):
        knowledge_chunks.append(PROGRAMS)

    # Check for injury-related queries
    if any(word in query_lower for word in ['pain', 'injury', 'hurt', 'sore']):
        knowledge_chunks.append(INJURY_PREVENTION)

    return "\n\n".join(knowledge_chunks)


def enhance_prompt_with_knowledge(base_prompt, user_data=None):
    """
    Add relevant knowledge to any prompt
    Use this in all your agents!
    """
    knowledge = get_relevant_knowledge(base_prompt, user_data)

    enhanced_prompt = f"""
EXPERT KNOWLEDGE BASE:
{knowledge}

YOUR TASK:
{base_prompt}

Use the knowledge above to provide accurate, expert-level coaching.
"""

    return enhanced_prompt


if __name__ == "__main__":
    # Test the knowledge base
    test_prompt = "Create a workout plan focusing on bench press"
    test_data = {"sleep_hours": 7, "soreness": 5}

    enhanced = enhance_prompt_with_knowledge(test_prompt, test_data)
    print("ENHANCED PROMPT:")
    print("=" * 70)
    print(enhanced)
