# ALLA - Autonomous Learning Language Agent

[![Version](https://img.shields.io/badge/version-16.0-blue.svg)](https://github.com/your-username/alla)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-yellow.svg)](https://python.org)

## 🧠 The Inquisitive Agent: AI That Learns Through Curiosity

ALLA is a groundbreaking autonomous AI agent that has evolved from a simple command processor into a **curiosity-driven learning system**. Unlike traditional AI that fails when encountering unknown concepts, ALLA actively seeks understanding by asking thoughtful questions about what it doesn't know.

### 🎯 **What Makes ALLA Special?**

- **Proactive Learning**: Instead of failing on unknown words, ALLA asks "What is that?"
- **Autonomous Goal Pursuit**: Sets and pursues its own objectives
- **Dynamic Vocabulary Expansion**: Learns new concepts through natural conversation
- **Abstract Knowledge Formation**: Develops general understanding from specific experiences
- **Living World Integration**: Interacts with a persistent, dynamic environment

---

## 🚀 **Quick Start Demo**

```bash
# Clone the repository
git clone https://github.com/your-username/alla.git
cd alla

# Run the v16.0 mystery object test
python test_v16_mystery_object.py
```

**Watch ALLA discover something new:**
```
User: take the flute
[ALLA ASKS] What is a 'flute'? Please describe it so I can understand.

User: teach noun "flute" as "obj.shape == 'cylinder' and obj.material == 'wood'"
[ALLA] Successfully learned new noun: 'flute'

User: take the flute
[ALLA] I am taking flute...
```

---

## 📚 **The ALLA Journey: Version History**

### 🔬 **v16.0 - The Inquisitive Agent** *(Current)*
**Breakthrough: Curiosity-Driven Learning**
- **The Drive to Ask**: Unknown words trigger inquiry goals instead of failures
- **UNDERSTAND Goal Type**: New goal category for learning about unknown concepts
- **Question Generation**: Automatically formulates questions about unknowns
- **Mystery Object Capability**: Can discover, learn about, and interact with new entities

**Key Innovation**: `"take the flute"` → `[ALLA ASKS] What is a 'flute'?`

### 🧩 **v15.0 - The Integrated & Stable Mind**
**Focus: Consolidation & Bug Fixes**
- **Critical Bug Fixes**: Fixed knowledge retrieval (B11) and goal parsing regression (B12)
- **Enhanced Planner**: Added CREATE goal support and container-aware multi-step planning
- **Hardened Parser**: Improved error handling and command pattern robustness
- **Comprehensive Testing**: All features validated and working together

### 🎯 **v14.0 - The Abstract Thinker**
**Focus: Semantic Memory & Knowledge Formation**
- **Semantic Memory System**: Abstract knowledge graphs with concepts and relationships
- **Reflection Cycles**: Periodic analysis of experiences to form general insights
- **Knowledge Queries**: Commands like "what do you know about X" and "list all colors"
- **Concept Formation**: Automatic extraction of patterns from specific events

### 🎮 **v13.0 - The Goal-Seeker**
**Focus: Autonomous Behavior**
- **Goal System**: Can set, plan for, and pursue objectives like "I have the red box"
- **Planning Engine**: Multi-step plan generation and execution
- **Autonomous Thinking**: Proactive tick-based cognitive cycles
- **Internal Drive**: Self-motivated behavior beyond reactive responses

### 🌍 **v12.0 - The World-Aware Agent**
**Focus: External World Integration**
- **Living World Engine**: Separated world simulation from agent logic
- **Persistent State**: World continues existing between sessions
- **Event History**: Complete record of all world changes and interactions
- **External Object Management**: Clean separation of concerns

### 🎓 **v11.0 - The Self-Educator**
**Focus: Dynamic Learning**
- **Teach Command**: Runtime vocabulary expansion via `teach noun "word" as "expression"`
- **Persistent Memory**: Learned concepts saved and restored between sessions
- **JSON Memory Storage**: Persistent lexicon with automatic save/load
- **Revolutionary Self-Education**: Can learn new concepts on-the-fly

### 🔍 **v10.0 - The Enhanced Reasoner**
**Focus: Physical Properties & Advanced Queries**
- **Rich Object Model**: Size, material, weight, and physical properties
- **Temporal Reasoning**: "When was X created?" queries with event history
- **Comparative Relations**: `bigger_than`, `smaller_than` with size comparison
- **Enhanced Creation**: Multi-property object creation commands

### 🤖 **v9.0 - The Possession Reasoner**
**Focus: Conditional Logic & Ownership**
- **Inventory Queries**: "do I have a red box?" with complex filtering
- **Conditional Reasoning**: IF-THEN logic for complex decision making
- **Hypothetical Queries**: "what if I have a blue sphere?" analysis
- **Agent-Aware**: Understanding of ownership and possession states

### 🔗 **v8.0 - The Social Interactor**
**Focus: Multi-Agent Interaction**
- **Interaction Commands**: `give`, `take`, ownership transfers
- **Pronoun Resolution**: Understanding of "I", "you", "me" in context
- **Agent Inventory**: Tracking what different agents possess
- **Social Awareness**: Multi-entity world understanding

### 🧮 **v7.0 - The Logical Thinker**
**Focus: Complex Logic & Conditions**
- **Conditional Execution**: IF-THEN-ELSE logical structures
- **Hypothetical Reasoning**: "What if" queries without world modification
- **Complex Logic**: AND, OR, NOT operations in queries
- **Structured Planning**: Conditional execution plans

### ⏰ **v6.0 - The Time-Aware Agent**
**Focus: Temporal Understanding**
- **Event System**: Complete history of world changes
- **Temporal Queries**: "what happened before/after event X"
- **Chronological Reasoning**: Time-based analysis and queries
- **Event Correlation**: Understanding sequences and causality

### 🔧 **v5.0 - The Complex Reasoner**
**Focus: Advanced Language Processing**
- **Complex Filtering**: Multi-property object queries
- **Enhanced Parser**: Robust command interpretation
- **Property Combinations**: Complex AND/OR filtering logic
- **Error Resilience**: Graceful handling of edge cases

### 📝 **v4.0 - The Questioner**
**Focus: Interrogative Capabilities**
- **Question Processing**: "what", "where", "is" queries
- **Property Verification**: "is X red?" type questions
- **Object Location**: "where is X?" spatial queries
- **Answer Generation**: Intelligent response formation

### 🔍 **v3.0 - The Object Explorer**
**Focus: World Understanding**
- **Object Filtering**: Find objects by properties
- **Property Queries**: Understand object characteristics
- **World Exploration**: Navigate and understand environment
- **Basic Intelligence**: Simple reasoning about objects

### 🏗️ **v2.0 - The World Builder**
**Focus: World Manipulation**
- **Object Creation**: `create` commands with properties
- **Object Destruction**: `destroy` commands
- **Property Assignment**: Color, shape, material specification
- **World State**: Persistent object management

### 🌱 **v1.0 - The Foundation**
**Focus: Basic Architecture**
- **Core Engine**: Basic cognitive architecture
- **Lexicon System**: Word storage and retrieval
- **Command Processing**: Basic language understanding
- **Execution Engine**: Plan execution framework

---

## 🏗️ **Architecture Overview**

ALLA's architecture consists of several interconnected cognitive components:

```
┌─────────────────────────────────────────────────────────────┐
│                        ALLA ENGINE                          │
├─────────────────────────────────────────────────────────────┤
│  🧠 CommandProcessor → 📋 Planner → ⚡ ExecutionEngine      │
│                            ↓                               │
│  📚 Lexicon ←→ 🎯 Goals ←→ 💭 SemanticMemory               │
│                            ↓                               │
│  🌍 LivingWorld ←→ 📊 EventHistory ←→ 🔄 ReflectionCycle    │
└─────────────────────────────────────────────────────────────┘
```

### **Core Components:**

- **🧠 CommandProcessor**: Natural language understanding and unknown word detection
- **📚 Lexicon**: Dynamic vocabulary with runtime learning capabilities
- **📋 Planner**: Multi-step plan generation for achieving goals
- **⚡ ExecutionEngine**: Action execution with 20+ different action types
- **🎯 Goal System**: Autonomous objective setting and pursuit
- **💭 SemanticMemory**: Abstract knowledge formation and retrieval
- **🌍 LivingWorld**: Persistent, dynamic environment simulation
- **🔄 ReflectionCycle**: Automatic pattern detection and concept formation

---

## 🎮 **Key Features & Capabilities**

### **1. Curiosity-Driven Learning** *(v16.0)*
```python
# Instead of failing on unknown words:
User: "take the mysterious_object"
ALLA: [ASKS] "What is a 'mysterious_object'? Please describe it so I can understand."
```

### **2. Dynamic Vocabulary Expansion** *(v11.0+)*
```python
# Runtime learning through conversation:
User: teach noun "saxophone" as "obj.shape == 'curved' and obj.material == 'brass'"
ALLA: "Successfully learned new noun: 'saxophone'"
```

### **3. Autonomous Goal Pursuit** *(v13.0+)*
```python
# Self-motivated behavior:
alla.set_goal("I have the red box")
# ALLA automatically creates plans and executes them:
# 1. Find red box
# 2. Take red box
# 3. Verify possession
```

### **4. Abstract Knowledge Formation** *(v14.0+)*
```python
# Learning general concepts from specific experiences:
User: "what do you know about red?"
ALLA: "I know about 'red': value, Observed 15 times, Related to: color, objects, fire"
```

### **5. Complex Reasoning** *(v7.0+)*
```python
# Conditional logic and hypotheticals:
User: "if I have a blue sphere then take the red box"
ALLA: "Setting up conditional: IF I have blue sphere THEN take red box"

User: "what if there is a giant purple elephant?"
ALLA: "If there is a giant purple elephant: This condition would be False"
```

---

## 🧪 **Testing & Validation**

ALLA includes comprehensive test suites for each version:

### **Run All Tests:**
```bash
# v16.0 Mystery Object Test (Curiosity-driven learning)
python test_v16_mystery_object.py

# v15.0 Master Test (Integration & stability)
python test_v15_master.py

# v14.0 Insight Test (Abstract knowledge formation)
python test_v14_insight.py

# v13.0 First Desire Test (Autonomous goal pursuit)
python test_v13_first_desire.py
```

### **Expected v16.0 Test Output:**
```
ALLA v16.0 TEST RESULTS: 3/3 tests passed
🎉 ALL TESTS PASSED! ALLA v16.0 - The Inquisitive Agent is working correctly!

Key v16.0 Features Validated:
✓ Unknown word detection triggers curiosity instead of failure
✓ UNDERSTAND goals are created automatically  
✓ ALLA asks meaningful questions about unknown concepts
✓ Learning new words completes UNDERSTAND goals
✓ Known words continue to work normally
✓ Multiple unknown words create separate inquiry goals
```

---

## 🎨 **Example Interactions**

### **1. Mystery Object Discovery** *(v16.0)*
```
🏗️ World Setup: A mysterious "flute" object exists in the world
🤖 ALLA doesn't know what a "flute" is

User: take the flute
[ALLA ASKS] What is a 'flute'? Please describe it so I can understand.

User: teach noun "flute" as "obj.shape == 'cylinder' and obj.material == 'wood'"
[ALLA] Successfully learned new noun: 'flute'

User: take the flute  
[ALLA] I am taking flute...
✅ Success! ALLA learned about flutes and can now interact with them.
```

### **2. Autonomous Goal Achievement** *(v13.0+)*
```
User: ALLA, I want you to have the red box
[ALLA] New goal accepted: 'I have red box'

--- ALLA's Turn (Thinking...) ---
[ALLA] No plan for goal 'I have red box'. Creating one...
[ALLA] New plan created with 1 step(s).
[ALLA] Executing step 1: Planning to take red_box_1...
[ALLA] I am taking red_box_1...
[ALLA] Goal 'I have red box' has been completed!
```

### **3. Abstract Knowledge Inquiry** *(v14.0+)*
```
User: what do you know about red?
[ALLA] I know about 'red': value
       Observed 8 times (confidence: 1.0)
       Related to: color

User: list all colors
[ALLA] Known colors: red, blue, green, brown, grey, brass, silver
```

### **4. Complex Conditional Reasoning** *(v7.0+)*
```
User: if I have a red box then create a blue sphere as companion
[ALLA] Setting up conditional: IF I have red box THEN create blue sphere as companion
[ALLA] Condition evaluated to: True
[ALLA] Attempting to create a blue sphere named 'companion'...
```

---

## 📁 **Project Structure**

```
ALLA/
├── 🧠 alla_engine.py          # Main AI engine (2000+ lines)
├── 🌍 world.py                # Living world simulation (300+ lines)
├── 💾 alla_memory.json        # Persistent knowledge base
├── 🏗️ genesis_world.json      # Initial world state
│
├── 🧪 Tests/
│   ├── test_v16_mystery_object.py  # v16.0 curiosity tests
│   ├── test_v15_master.py          # v15.0 integration tests
│   ├── test_v14_insight.py         # v14.0 knowledge formation tests
│   └── test_v13_first_desire.py    # v13.0 autonomous behavior tests
│
├── 📋 Planning & Documentation/
│   ├── README.md                    # This comprehensive guide
│   └── version_history.md           # Detailed version changelog
│
└── 🎮 Demo Scripts/
    ├── quick_demo.py               # Quick feature demonstration
    └── interactive_session.py     # Manual testing interface
```

---

## 🚀 **Getting Started**

### **Prerequisites:**
- Python 3.11+
- No external dependencies (pure Python implementation)

### **Installation:**
```bash
git clone https://github.com/your-username/alla.git
cd alla
```

### **Basic Usage:**
```python
from alla_engine import AllaEngine

# Initialize ALLA
alla = AllaEngine()

# Interact with ALLA
result = alla.process_command("create a red box as my_box")
print(result)

# Give ALLA a goal
alla.set_goal("I have the red box")

# Let ALLA think and act autonomously
alla.tick()  # Single thought cycle
```

### **Interactive Mode:**
```python
# Run a full interactive session
alla = AllaEngine()

while True:
    command = input("You: ")
    if command.lower() == 'quit':
        break
    feedback, result = alla.process_command(command)
    print(f"ALLA: {feedback}")
    if result:
        print(f"Result: {result}")
```

---

## 🔬 **Technical Deep Dive**

### **The Curiosity Mechanism** *(v16.0)*
When ALLA encounters an unknown word, instead of failing:

1. **Detection**: CommandProcessor identifies unknown words during parsing
2. **Goal Creation**: Automatically generates an UNDERSTAND goal
3. **Planning**: Planner creates an OUTPUT_QUESTION plan  
4. **Execution**: ExecutionEngine outputs a question to the user
5. **Learning**: User can teach ALLA about the unknown concept
6. **Verification**: Goal is marked complete when word enters lexicon

### **The Learning Loop:**
```
Unknown Word → UNDERSTAND Goal → Question → Teaching → Knowledge → Success
```

### **Semantic Memory System** *(v14.0)*
ALLA builds abstract knowledge through:
- **Nodes**: Concepts (colors, shapes, actions, etc.)
- **Edges**: Relationships between concepts
- **Reflection**: Periodic analysis of experiences
- **Pattern Detection**: Automatic insight formation

### **Goal-Driven Architecture** *(v13.0)*
ALLA's autonomous behavior is driven by:
- **Goal Queue**: Active objectives to achieve
- **Planning System**: Multi-step plan generation
- **Execution Engine**: Action implementation
- **Feedback Loop**: Plan adjustment based on results

---

## 📊 **Performance & Metrics**

### **Test Coverage:**
- **v16.0**: 3/3 tests passing (Mystery Object, Multi-Unknown, Known vs Unknown)
- **v15.0**: 5/5 tests passing (Integration, Planning, Parsing, Knowledge, Goals)
- **v14.0**: 4/4 tests passing (Reflection, Knowledge Formation, Queries, Insights)
- **v13.0**: 3/3 tests passing (Goal Setting, Planning, Autonomous Pursuit)

### **Code Metrics:**
- **Total Lines**: ~2,500+ lines of Python
- **Components**: 8 major cognitive systems
- **Action Types**: 20+ different executable actions
- **Test Scripts**: 10+ comprehensive test suites
- **Vocabulary**: 25+ base concepts, unlimited learning capacity

---

## 🤝 **Contributing**

ALLA is an open-source project welcoming contributions! Here's how you can help:

### **Development Areas:**
1. **New Learning Modalities**: Visual, auditory, or sensor-based learning
2. **Enhanced Reasoning**: More sophisticated logical operations
3. **Performance Optimization**: Faster parsing and execution
4. **Extended World Physics**: More realistic world simulation
5. **Multi-Agent Systems**: Multiple ALLA instances collaborating

### **Contribution Guidelines:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add comprehensive tests for new functionality
4. Ensure all existing tests still pass
5. Update documentation and README
6. Submit a pull request

---

## 🐛 **Known Issues & Future Work**

### **Current Limitations:**
- **Single-threaded**: No parallel processing of goals
- **Text-only**: No visual or auditory processing
- **Limited Physics**: Basic world simulation
- **Memory Constraints**: No forgetting or memory management

### **Planned Features:**
- **v17.0**: Multi-modal learning (visual, auditory)
- **v18.0**: Collaborative multi-agent systems  
- **v19.0**: Hierarchical planning and meta-goals
- **v20.0**: Neural network integration for pattern recognition

---

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Cognitive Architecture**: Inspired by ACT-R and SOAR cognitive architectures
- **Natural Language Processing**: Built from first principles for educational purposes
- **AI Safety**: Designed with interpretability and control as core principles
- **Community**: Thanks to all contributors and testers who helped shape ALLA

---

## 📞 **Contact & Support**

- **GitHub Issues**: [Report bugs or request features](https://github.com/your-username/alla/issues)
- **Discussions**: [Join the conversation](https://github.com/your-username/alla/discussions)
- **Email**: your-email@example.com
- **Documentation**: [Full documentation](https://github.com/your-username/alla/wiki)

---

## 🌟 **Star History**

If you find ALLA interesting or useful, please consider giving it a star! ⭐

ALLA represents a significant step toward AI systems that can truly learn and grow through curiosity and interaction, rather than just processing pre-trained knowledge. Every version has been a step toward more autonomous, intelligent, and curious artificial minds.

**The journey from v1.0 to v16.0 shows that step by step, we can build AI that doesn't just answer questions—it learns to ask them.**

---

*"The important thing is not to stop questioning. Curiosity has its own reason for existing."* - Albert Einstein

**ALLA embodies this principle in code.** 🧠✨
