# Edited UML Diagrams for Python Tkinter Desktop Application

## 1. Use Case Diagram (Generalization)

The Use Case Diagram is largely application-agnostic, but the "System" actor is generalized to "Background Service" to better reflect a desktop application's background process (e.g., a scheduled Python script or a separate thread).

```mermaid
---
title: Use Case Diagram - Productivity App (Tkinter Ready)
---

graph TB

    User((User))
    Student((Student<br/>extends User))
    Service[Background<br/>Service/Scheduler]

    User --> UC1[Create Goal]
    User --> UC2[Create Task]
    User --> UC3[Complete Task]
    User --> UC4[View Calendar]
    User --> UC5[View Dashboard]
    User --> UC6[Set Reminders]
    User --> UC7[Edit Task]
    User --> UC8[Delete Task]
    User --> UC9[Archive Goal]
    User --> UC10[View Task History]

    Student --> UC11[Create Course]
    Student --> UC12[Add Assignment]
    Student --> UC13[Schedule Exam]
    Student --> UC14[Track Study Sessions]
    Student --> UC15[View Academic Calendar]

    Service --> UC16[Send Task Reminder]
    Service --> UC17[Send Streak Warning]
    Service --> UC18[Send Achievement<br/>Notification]
    Service --> UC19[Calculate Daily Streaks]

    UC2 -.includes.-> UC1
    UC12 -.includes.-> UC11
    UC5 -.includes.-> UC19
    UC16 -.extends.-> UC6

    style User fill:#e1f5ff
    style Student fill:#fff4e1
    style Service fill:#ffe1e1
```

## 2. Class Diagram (Domain Model)

The Class Diagram defines the core data model and is highly suitable for implementation using Python classes and a local SQLite database. No significant changes are required, as the model is domain-centric.

```mermaid
---
title: Class Diagram - Core Data Models (Python Ready)
---

classDiagram

    class User {
        +String userId
        +String name
        +String email
        +Boolean isStudentMode
        +NotificationPreferences preferences
        +DateTime createdAt
        +toggleStudentMode()
        +updatePreferences()
    }

    class Goal {
        +String goalId
        +String userId
        +String title
        +String description
        +GoalCategory category
        +String colorHex
        +FrequencyType frequency
        +DateTime createdAt
        +Boolean isArchived
        +Int currentStreak
        +Int longestStreak
        +archive()
        +updateStreak()
        +calculateCompletionRate()
    }

    class Task {
        +String taskId
        +String goalId
        +String userId
        +String title
        +String description
        +DateTime dueDateTime
        +Int durationMinutes
        +Priority priority
        +RecurrenceRule recurrence
        +Boolean isCompleted
        +DateTime completedAt
        +TaskType type
        +complete()
        +snooze()
        +generateNextInstance()
    }

    class RecurrenceRule {
        +RecurrenceType type
        +Int interval
        +List~DayOfWeek~ daysOfWeek
        +DateTime endDate
        +Int maxOccurrences
        +getNextOccurrence()
        +shouldRepeat()
    }

    class Reminder {
        +String reminderId
        +String taskId
        +DateTime reminderTime
        +Int minutesBefore
        +Boolean isSent
        +ReminderType type
        +schedule()
        +cancel()
    }

    class Course {
        +String courseId
        +String userId
        +String courseName
        +String courseCode
        +String instructor
        +Int credits
        +Semester semester
        +String colorHex
        +List~ClassSchedule~ schedule
        +calculateGrade()
    }

    class Assignment {
        +String assignmentId
        +String courseId
        +String title
        +DateTime dueDate
        +Int maxPoints
        +Int earnedPoints
        +AssignmentType type
        +Boolean isCompleted
        +submit()
    }

    class Exam {
        +String examId
        +String courseId
        +String title
        +DateTime examDate
        +String location
        +Int maxPoints
        +Int earnedPoints
        +ExamType type
    }

    class Streak {
        +String streakId
        +String goalId
        +Int currentCount
        +Int longestCount
        +DateTime lastCompletedDate
        +List~DateTime~ missedDates
        +increment()
        +break()
        +checkMissedDays()
    }

    class Notification {
        +String notificationId
        +String userId
        +String title
        +String body
        +NotificationType type
        +DateTime scheduledTime
        +Boolean isSent
        +String deepLink
        +send()
    }

    class InsightData {
        +String userId
        +DateTime date
        +Int tasksCompleted
        +Int tasksScheduled
        +Float completionRate
        +Int activeStreaks
        +Map~String,Int~ timePerGoal
        +calculate()
    }

    User "1" --> "*" Goal : owns
    User "1" --> "*" Task : owns
    User "1" --> "*" Course : enrolledIn
    User "1" --> "*" Notification : receives
    Goal "1" --> "*" Task : contains
    Goal "1" --> "1" Streak : tracks
    Task "1" --> "0..1" RecurrenceRule : follows
    Task "1" --> "*" Reminder : has
    Task "0..1" --> "1" Course : linkedTo
    Course "1" --> "*" Assignment : has
    Course "1" --> "*" Exam : schedules
    Assignment --|> Task : extends
    Exam --|> Task : extends
    Goal --> InsightData : analyzed
    Task --> InsightData : analyzed
```

## 3. Component Diagram (Python Tkinter Architecture)

The original Android Architecture Component Diagram is replaced with a **Component Diagram** that follows a common pattern for Python desktop applications, such as a Model-View-Controller (MVC) or Model-View-Presenter (MVP) variant, using a Service Layer and a local SQLite database.

```mermaid
---
title: Component Diagram - Python Tkinter Application Architecture (MVP/Service Layer)
---

graph TD
    subgraph Presentation Layer
        TkinterUI[Tkinter Views/Widgets]
        Presenter[Presenter/Controller]
    end

    subgraph Application/Domain Layer
        ServiceLayer["Service Layer<br/>(Use Cases/Business Logic)"]
    end

    subgraph Data Layer
        Repository["Repository Layer<br/>(Data Access Objects)"]
        SQLiteDB[(SQLite Database)]
    end

    subgraph Infrastructure/System
        Scheduler["Background Scheduler<br/>(e.g., APScheduler/Threading)"]
        NotificationSystem["OS Notification System<br/>(e.g., win10toast)"]
    end

    TkinterUI -->|User Actions| Presenter
    Presenter -->|Update View| TkinterUI
    Presenter -->|Request Data/Action| ServiceLayer
    ServiceLayer -->|CRUD Operations| Repository
    Repository -->|SQL Queries| SQLiteDB
    SQLiteDB -->|Results| Repository
    Repository -->|Data Models| ServiceLayer
    ServiceLayer -->|Results/Status| Presenter

    ServiceLayer -->|Schedule Task/Check| Scheduler
    Scheduler -->|Trigger Check| ServiceLayer
    ServiceLayer -->|Send Notification| NotificationSystem

    style TkinterUI fill:#e1f5ff
    style Presenter fill:#fff4e1
    style ServiceLayer fill:#fff9c4
    style Repository fill:#c8e6c9
    style SQLiteDB fill:#a5d6a7
    style Scheduler fill:#ffe0b2
    style NotificationSystem fill:#ffccbc
```

## 4. Sequence Diagram: Task Completion Flow (Tkinter Ready)

The sequence diagram is updated to reflect the Python/Tkinter architecture components.

```mermaid
---
title: Sequence Diagram - Task Completion Flow (Tkinter Ready)
---

sequenceDiagram

    actor User
    participant View as TkinterView
    participant Controller as Presenter/Controller
    participant Service as TaskService
    participant Repo as Repository
    participant DB as SQLite Database
    participant Scheduler as Background Scheduler
    participant Notifier as OS Notifier

    User->>View: Click "Complete Task"
    View->>Controller: completeTask(taskId)
    Controller->>Service: executeCompletion(taskId)

    Service->>Repo: getTaskById(taskId)
    Repo->>DB: SELECT * FROM tasks WHERE id=?
    DB-->>Repo: Task Data
    Repo-->>Service: Task Model

    Service->>Repo: updateTask(task.isCompleted=True)
    Repo->>DB: UPDATE tasks SET is_completed=1
    DB-->>Repo: Success

    alt Task has associated Goal
        Service->>Repo: getGoalAndStreak(goalId)
        Repo->>DB: Query Goal and Streak
        DB-->>Repo: Data
        Repo-->>Service: Models

        Service->>Repo: updateStreak(streak.increment())
        Repo->>DB: UPDATE streaks SET current_count++
        DB-->>Repo: Success

        alt Streak milestone reached
            Service->>Notifier: sendAchievementNotification()
            Notifier-->>User: "🎉 7-day streak!"
        end
    end

    alt Task is recurring
        Service->>Service: generateNextInstance(task)
        Service->>Repo: saveTask(newTask)
        Repo->>DB: INSERT next task instance
        DB-->>Repo: New task created

        Service->>Scheduler: scheduleReminder(newTask)
        Scheduler-->>Scheduler: Schedule next job
    end

    Service-->>Controller: CompletionResult
    Controller-->>View: Update UI state
    View-->>User: Show completion animation & Update task list
```

## 5. Sequence Diagram: Streak Warning System (Tkinter Ready)

The streak warning system is adapted to use a generic `Background Scheduler` and `Worker` instead of Android's `WorkManager`.

```mermaid
---
title: Sequence Diagram - Streak Warning System (Tkinter Ready)
---

sequenceDiagram

    participant Scheduler as Background Scheduler
    participant Worker as DailyStreakWorker
    participant Service as StreakService
    participant Repo as Repository
    participant DB as SQLite Database
    participant Notifier as OS Notifier
    actor User

    Note over Scheduler: Scheduled Daily Check (e.g., 11:00 PM)
    Scheduler->>Worker: Execute daily check

    Worker->>Service: checkAllStreaks()
    Service->>Repo: getAllActiveStreaks()
    Repo->>DB: SELECT * FROM streaks WHERE active=1
    DB-->>Repo: Streak List
    Repo-->>Service: Streak Models

    loop For each Streak
        Service->>Service: checkGoalCompletion(streak)
        alt Goal not completed today
            Service->>Service: determineWarningLevel()
            alt First missed day
                Service->>Notifier: sendNotification(DAILY_WARNING)
                Notifier-->>User: "You missed [Goal] today 🤔"
            else 3 consecutive days
                Service->>Notifier: sendNotification(URGENT_WARNING)
                Notifier-->>User: "3-day streak broken! Don't give up! 💪"
            end

            Service->>Repo: addMissedDate(streakId, today)
            Repo->>DB: UPDATE streaks

            alt Streak was active
                Service->>Repo: breakStreak(streakId)
                Repo->>DB: UPDATE streaks SET current_count=0
            end
        else Tasks completed
            Service->>Repo: clearMissedDates(streakId)
            Repo->>DB: UPDATE streaks
        end
    end

    Worker->>Scheduler: Schedule next run (tomorrow 11 PM)
    Worker-->>Scheduler: Success
```

## 6. State Diagram: Task Lifecycle

The Task Lifecycle State Diagram is largely fine, but the notes are generalized to remove Android-specific context.

```mermaid
---
title: State Diagram - Task Lifecycle (Tkinter Ready)
---

stateDiagram-v2

    [*] --> Created: User creates task
    Created --> Scheduled: Set due date/time
    Created --> Pending: No due date (anytime task)

    Scheduled --> Upcoming: Due in > 24 hours
    Scheduled --> Today: Due within 24 hours
    Upcoming --> Today: Time passes
    Today --> Overdue: Due time passed, not completed
    Today --> InProgress: User starts task
    Upcoming --> InProgress: User starts task early
    InProgress --> Paused: User pauses
    Paused --> InProgress: User resumes

    InProgress --> Completed: User marks complete
    Today --> Completed: User marks complete
    Upcoming --> Completed: User marks complete early
    Pending --> Completed: User marks complete
    Overdue --> Completed: User marks complete late

    Overdue --> Snoozed: User snoozes
    Snoozed --> Today: Snooze time reached

    Scheduled --> Cancelled: User cancels
    Today --> Cancelled: User cancels
    Overdue --> Cancelled: User cancels

    Completed --> [*]: End state
    Cancelled --> [*]: End state

    Completed --> Recurring: If recurring task
    Recurring --> Created: Generate next instance

    note right of Overdue
        Triggers OS notification
        if goal-linked task
    end note

    note right of Completed
        Updates streak if
        goal-linked task
    end note

    note right of Recurring
        Creates new task instance
        based on recurrence rule
    end note
```

## 7. Activity Diagram: Create Task Workflow

The Activity Diagram is mostly a user flow, but the final steps mentioning `WorkManager` are generalized to `Scheduler`.

```mermaid
---
title: Activity Diagram - Create Task Workflow (Tkinter Ready)
---

graph TD

    Start([User taps Create Task]) --> CheckMode{Student Mode<br/>Enabled?}

    CheckMode -->|Yes| SelectType[Select Task Type:<br/>- Free Task<br/>- Goal Task<br/>- Assignment<br/>- Study Session]
    CheckMode -->|No| SelectTypeBasic[Select Task Type:<br/>- Free Task<br/>- Goal Task]

    SelectType --> IsAssignment{Assignment<br/>Selected?}
    SelectTypeBasic --> IsGoalTask{Goal Task<br/>Selected?}

    IsAssignment -->|Yes| SelectCourse[Select Course]
    IsAssignment -->|No| IsStudySession{Study Session<br/>Selected?}

    IsStudySession -->|Yes| SelectCourse
    IsStudySession -->|No| IsGoalTask

    SelectCourse --> EnterAssignmentDetails[Enter Assignment Details:<br/>- Title<br/>- Due Date<br/>- Points]

    IsGoalTask -->|Yes| SelectGoal{Goal<br/>Exists?}
    IsGoalTask -->|No| EnterBasicDetails

    SelectGoal -->|Yes| ChooseGoal[Choose from Goal List]
    SelectGoal -->|No| CreateGoal[Create New Goal]

    CreateGoal --> EnterGoalDetails[Enter Goal Details:<br/>- Title<br/>- Category<br/>- Frequency<br/>- Color]
    EnterGoalDetails --> SaveGoal[Save Goal]
    SaveGoal --> ChooseGoal

    ChooseGoal --> EnterTaskDetails[Enter Task Details:<br/>- Title<br/>- Description]
    EnterAssignmentDetails --> EnterTaskDetails
    EnterBasicDetails[Enter Task Details:<br/>- Title<br/>- Description] --> EnterTaskDetails

    EnterTaskDetails --> SetSchedule[Set Schedule:<br/>- Due Date<br/>- Time<br/>- Duration]

    SetSchedule --> IsRecurring{Recurring<br/>Task?}

    IsRecurring -->|Yes| SetRecurrence[Set Recurrence:<br/>- Frequency<br/>- Days<br/>- End Date]
    IsRecurring -->|No| SetReminder

    SetRecurrence --> SetReminder{Add<br/>Reminder?}

    SetReminder -->|Yes| ConfigureReminder[Configure Reminder:<br/>- Time Before<br/>- Notification Type]
    SetReminder -->|No| SetPriority

    ConfigureReminder --> SetPriority[Set Priority:<br/>- Low<br/>- Medium<br/>- High<br/>- Urgent]

    SetPriority --> ReviewTask[Review Task Summary]

    ReviewTask --> ValidateInput{All Required<br/>Fields Valid?}

    ValidateInput -->|No| ShowError[Show Validation Errors]
    ShowError --> EnterTaskDetails

    ValidateInput -->|Yes| SaveTask[Save Task to Database]

    SaveTask --> ScheduleNotifications{Has<br/>Reminders?}

    ScheduleNotifications -->|Yes| CreateSchedulerJob[Schedule Background<br/>Job for Notifications]
    ScheduleNotifications -->|No| CheckRecurringSchedule

    CreateSchedulerJob --> CheckRecurringSchedule{Is<br/>Recurring?}

    CheckRecurringSchedule -->|Yes| GenerateInstances[Generate Next<br/>Task Instance]
    CheckRecurringSchedule -->|No| UpdateUI

    GenerateInstances --> UpdateUI[Update Calendar<br/>and Task List UI]

    UpdateUI --> ShowSuccess[Show Success Message]

    ShowSuccess --> End([Task Created])

    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style ShowError fill:#ffcdd2
    style SaveTask fill:#fff9c4
    style CreateSchedulerJob fill:#fff9c4
    style GenerateInstances fill:#fff9c4
```

## 8. Entity Relationship Diagram (Database Schema)

The ER Diagram is excellent for defining the SQLite database schema. It is fully compatible with a Python desktop application using a library like `sqlite3` or an ORM like `SQLAlchemy`. No changes are needed.

```mermaid
---
title: Entity Relationship Diagram (SQLite Ready)
---

erDiagram

    USER ||--o{ GOAL : owns
    USER ||--o{ TASK : creates
    USER ||--o{ COURSE : enrolls
    USER ||--|| USER_PREFERENCES : has
    GOAL ||--o{ TASK : contains
    GOAL ||--|| STREAK : tracks
    GOAL ||--o{ GOAL_COMPLETION_HISTORY : records
    TASK ||--o{ REMINDER : has
    TASK ||--o| RECURRENCE_RULE : follows
    TASK ||--o{ TASK_COMPLETION_HISTORY : logs
    COURSE ||--o{ ASSIGNMENT : includes
    COURSE ||--o{ EXAM : schedules
    COURSE ||--o{ CLASS_SCHEDULE : has
    COURSE ||--o{ STUDY_SESSION : generates
    ASSIGNMENT ||--|| TASK : extends
    EXAM ||--|| TASK : extends
    STUDY_SESSION ||--|| TASK : extends

    USER {
        string user_id PK
        string name
        string email
        boolean is_student_mode
        datetime created_at
        datetime updated_at
    }

    USER_PREFERENCES {
        string pref_id PK
        string user_id FK
        boolean notifications_enabled
        string notification_sound
        int quiet_hours_start
        int quiet_hours_end
        string theme_mode
        boolean vibration_enabled
        int default_reminder_minutes
    }

    GOAL {
        string goal_id PK
        string user_id FK
        string title
        string description
        string category
        string color_hex
        string frequency_type
        int target_per_week
        datetime created_at
        boolean is_archived
        datetime archived_at
    }

    STREAK {
        string streak_id PK
        string goal_id FK
        int current_count
        int longest_count
        datetime last_completed_date
        datetime longest_streak_start
        datetime longest_streak_end
        string missed_dates_json
    }

    GOAL_COMPLETION_HISTORY {
        string history_id PK
        string goal_id FK
        date completion_date
        int tasks_completed
        int tasks_scheduled
        float completion_percentage
    }

    TASK {
        string task_id PK
        string user_id FK
        string goal_id FK "nullable"
        string course_id FK "nullable"
        string title
        string description
        datetime due_date_time
        int duration_minutes
        string priority
        string task_type
        boolean is_completed
        datetime completed_at
        datetime created_at
        datetime updated_at
        string parent_task_id FK "for recurring"
    }

    RECURRENCE_RULE {
        string rule_id PK
        string task_id FK
        string recurrence_type
        int interval
        string days_of_week_json
        datetime start_date
        datetime end_date
        int max_occurrences
        int occurrences_count
    }

    REMINDER {
        string reminder_id PK
        string task_id FK
        datetime reminder_time
        int minutes_before
        boolean is_sent
        string reminder_type
        datetime created_at
    }

    TASK_COMPLETION_HISTORY {
        string completion_id PK
        string task_id FK
        datetime completed_at
        int time_taken_minutes
        string notes
    }

    COURSE {
        string course_id PK
        string user_id FK
        string course_name
        string course_code
        string instructor
        int credits
        string semester
        int semester_year
        datetime semester_start
        datetime semester_end
        string color_hex
        float current_grade
        boolean is_archived
    }

    CLASS_SCHEDULE {
        string schedule_id PK
        string course_id FK
        string day_of_week
        time start_time
        time end_time
        string location
        string schedule_type
    }

    ASSIGNMENT {
        string assignment_id PK
        string task_id FK
        string course_id FK
        string assignment_type
        int max_points
        int earned_points
        float weight_percentage
        datetime submitted_at
    }

    EXAM {
        string exam_id PK
        string task_id FK
        string course_id FK
        string exam_type
        string location
        int max_points
        int earned_points
        float weight_percentage
        string topics_json
    }

    STUDY_SESSION {
        string session_id PK
        string task_id FK
        string course_id FK
        int planned_minutes
        int actual_minutes
        string topics_covered_json
    }
```

## 9. Deployment Diagram (Tkinter Ready)

The original Android Deployment Diagram is replaced with a simple **Deployment Diagram** for a Python Tkinter application on Windows 10.

```mermaid
---
title: Deployment Diagram - Python Tkinter on Windows 10
---

graph TD
    subgraph Windows 10 PC
        OS["Operating System<br/>(Windows 10)"]
        Python["Python Environment<br/>(Interpreter/Libraries)"]
        App["Tkinter Desktop Application<br/>(Main Executable)"]
        SQLite["(Local SQLite Database File)"]
        OS_Notifier[Windows Notification System]
    end

    User((User)) -->|Interacts with UI| App
    App -->|Executes Code| Python
    Python -->|Read/Write Data| SQLite
    Python -->|Send Notifications| OS_Notifier
    Python -->|File System Access| OS

    style OS fill:#e1f5ff
    style Python fill:#fff4e1
    style App fill:#c8e6c9
    style SQLite fill:#a5d6a7
    style OS_Notifier fill:#ffccbc
```
