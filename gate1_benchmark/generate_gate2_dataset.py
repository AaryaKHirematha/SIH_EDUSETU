import json

dataset = []

# ================= PHYSICS (25 items) =================
physics_items = [
    ("PHY_001", "short", "sentence", "Force is equal to mass times acceleration.", ["terminology"], [], [], [{"en": "force", "hi": "बल", "kn": "ಬಲ"}, {"en": "mass", "hi": "द्रव्यमान", "kn": "ದ್ರವ್ಯರಾಶಿ"}]),
    ("PHY_002", "short", "sentence", "The mass of the object is exactly 5 kg.", ["units"], [], [], [{"en": "mass", "hi": "द्रव्यमान", "kn": "ದ್ರವ್ಯರಾಶಿ"}]),
    ("PHY_003", "medium", "sentence", "The famous equation E = mc² describes the relationship between energy and mass.", ["formula", "morphology"], ["E = mc²"], [], [{"en": "energy", "hi": "ऊर्जा"}, {"en": "mass", "hi": "द्रव्यमान", "kn": "ದ್ರವ್ಯರಾಶಿ"}]),
    ("PHY_004", "short", "sentence", "Gravity on Earth is approximately 9.8 m/s².", ["formula", "units"], ["9.8 m/s²"], [], [{"en": "gravity", "hi": "गुरुत्वाकर्षण", "kn": "ಗುರುತ್ವಾಕರ್ಷಣೆ"}]),
    ("PHY_005", "short", "definition", "Momentum is equal to mass times velocity.", ["terminology"], [], [], [{"en": "momentum", "hi": "संवेग", "kn": "ಆವೇಗ"}, {"en": "velocity", "hi": "वेग", "kn": "ವೇಗ"}]),
    ("PHY_006", "medium", "sentence", "According to Newton's second law, F = ma.", ["formula"], ["F = ma"], [], []),
    ("PHY_007", "long", "paragraph", "Work is done when a force that is applied to an object moves that object. The work is calculated by multiplying the force by the amount of movement of an object (W = F * d).", ["formula", "terminology"], ["W = F * d"], [], [{"en": "force", "hi": "बल", "kn": "ಬಲ"}, {"en": "work", "hi": "कार्य"}]),
    ("PHY_008", "short", "sentence", "The unit of force is the Newton (N).", ["units"], ["(N)"], [], [{"en": "force", "hi": "बल", "kn": "ಬಲ"}]),
    ("PHY_009", "medium", "sentence", "Kinetic energy is the energy that an object possesses due to its motion.", ["definition"], [], [], [{"en": "kinetic energy", "hi": "गतिज ऊर्जा", "kn": "ಚಲನ ಶಕ್ತಿ"}]),
    ("PHY_010", "medium", "sentence", "Potential energy is stored energy that depends upon the relative position of various parts of a system.", ["definition"], [], [], [{"en": "potential energy", "hi": "स्थितिज ऊर्जा", "kn": "ಸ್ಥಿತಿ ಶಕ್ತಿ"}]),
    ("PHY_011", "medium", "explanation", "When a car accelerates, its velocity increases over time.", ["terminology"], [], [], [{"en": "velocity", "hi": "वेग"}, {"en": "accelerates", "hi": "त्वरित"}]),
    ("PHY_012", "short", "sentence", "The speed of light in a vacuum is 3 × 10⁸ m/s.", ["formula", "units"], ["3 × 10⁸ m/s"], [], []),
    ("PHY_013", "medium", "sentence", "Friction is the force resisting the relative motion of solid surfaces, fluid layers, and material elements sliding against each other.", ["definition"], [], [], [{"en": "friction", "hi": "घर्षण"}]),
    ("PHY_014", "short", "sentence", "Power is the rate at which work is done.", ["definition"], [], [], [{"en": "power", "hi": "शक्ति"}]),
    ("PHY_015", "medium", "sentence", "The formula for power is P = W / t, where W is work and t is time.", ["formula"], ["P = W / t", "W", "t"], [], []),
    ("PHY_016", "long", "paragraph", "Thermodynamics is the branch of physics that deals with heat, work, and temperature, and their relation to energy, radiation, and properties of matter.", ["definition", "terminology"], [], [], [{"en": "thermodynamics", "hi": "ऊष्मागतिकी"}]),
    ("PHY_017", "medium", "explanation", "A vector quantity has both magnitude and direction, whereas a scalar quantity has only magnitude.", ["terminology"], [], [], [{"en": "vector", "hi": "सदिश"}, {"en": "scalar", "hi": "अदिश"}]),
    ("PHY_018", "short", "sentence", "Voltage is the difference in electric potential between two points.", ["definition"], [], [], [{"en": "voltage", "hi": "वोल्टेज"}]),
    ("PHY_019", "short", "sentence", "Ohm's law states that V = IR.", ["formula"], ["V = IR"], [], []),
    ("PHY_020", "medium", "sentence", "Magnetic fields are produced by moving electric charges and the intrinsic magnetic moments of elementary particles.", ["terminology"], [], [], [{"en": "magnetic fields", "hi": "चुंबकीय क्षेत्र"}]),
    ("PHY_021", "medium", "sentence", "The standard unit of electrical resistance is the ohm (Ω).", ["units", "formula"], ["(Ω)"], [], [{"en": "resistance", "hi": "प्रतिरोध"}]),
    ("PHY_022", "short", "sentence", "Density is defined as mass per unit volume.", ["definition"], [], [], [{"en": "density", "hi": "घनत्व"}, {"en": "volume", "hi": "आयतन"}]),
    ("PHY_023", "medium", "explanation", "If the net force on an object is zero, its acceleration is also zero.", ["terminology"], [], [], [{"en": "net force", "hi": "शुद्ध बल"}, {"en": "acceleration", "hi": "त्वरण", "kn": "ವೇಗವರ್ಧನೆ"}]),
    ("PHY_024", "medium", "sentence", "The wavelength of the wave is inversely proportional to its frequency.", ["terminology"], [], [], [{"en": "wavelength", "hi": "तरंगदैर्ध्य"}, {"en": "frequency", "hi": "आवृत्ति"}]),
    ("PHY_025", "short", "sentence", "An object in free fall experiences an acceleration of 9.8 m/s².", ["formula", "units"], ["9.8 m/s²"], [], [])
]

# ================= MATHEMATICS (30 items) =================
math_items = [
    ("MAT_001", "medium", "sentence", "The quadratic equation can be solved using the quadratic formula.", ["terminology", "hallucination_risk"], [], [], [{"en": "quadratic equation", "hi": "द्विघात समीकरण", "kn": "ವರ್ಗ ಸಮೀಕರಣ"}, {"en": "quadratic formula", "hi": "द्विघात सूत्र", "kn": "ವರ್ಗ ಸೂತ್ರ"}]),
    ("MAT_002", "medium", "definition", "A polynomial is an algebraic expression consisting of variables and coefficients.", ["terminology"], [], [], [{"en": "polynomial", "hi": "बहुपद", "kn": "ಬಹುಪದ"}, {"en": "algebraic expression", "hi": "बीजगणितीय व्यंजक", "kn": "ಬೀಜಗಣಿತದ ಅಭಿವ್ಯಕ್ತಿ"}]),
    ("MAT_003", "medium", "sentence", "The derivative of a function represents its rate of change.", ["terminology"], [], [], [{"en": "derivative", "hi": "अवकलज", "kn": "ವ್ಯುತ್ಪನ್ನ"}, {"en": "function", "hi": "फलन", "kn": "ಕಾರ್ಯ"}]),
    ("MAT_004", "short", "sentence", "Integration is used to calculate area under a curve.", ["terminology"], [], [], [{"en": "integration", "hi": "समाकलन", "kn": "ಅನುಕಲನ"}]),
    ("MAT_005", "short", "definition", "A matrix is a rectangular arrangement of numbers.", ["terminology"], [], [], [{"en": "matrix", "hi": "आव्यूह", "kn": "ಮಾತೃಕೆ"}]),
    ("MAT_006", "short", "sentence", "The coefficient of x in the equation is 5.", ["terminology", "formula"], ["x"], [], [{"en": "coefficient", "hi": "गुणांक", "kn": "ಗುಣಾಂಕ"}]),
    ("MAT_007", "medium", "explanation", "To find the roots of the equation x² - 5x + 6 = 0, we can factorize it.", ["formula"], ["x² - 5x + 6 = 0"], [], [{"en": "roots", "hi": "मूल"}]),
    ("MAT_008", "short", "sentence", "The Pythagorean theorem states that a² + b² = c².", ["formula"], ["a² + b² = c²"], [], []),
    ("MAT_009", "medium", "sentence", "In a right-angled triangle, the sine of an angle is the ratio of the opposite side to the hypotenuse.", ["terminology"], [], [], [{"en": "sine", "hi": "ज्या"}, {"en": "hypotenuse", "hi": "कर्ण"}]),
    ("MAT_010", "medium", "sentence", "The probability of an impossible event is 0, and the probability of a certain event is 1.", ["terminology"], [], [], [{"en": "probability", "hi": "प्रायिकता"}]),
    ("MAT_011", "long", "paragraph", "A linear equation in two variables describes a line on a Cartesian coordinate plane. The standard form is Ax + By = C, where A, B, and C are constants, and x and y are variables.", ["terminology", "formula"], ["Ax + By = C", "A", "B", "C", "x", "y"], [], [{"en": "linear equation", "hi": "रैखिक समीकरण", "kn": "ರೇಖಾತ್ಮಕ ಸಮೀಕರಣ"}, {"en": "variables", "hi": "चर"}]),
    ("MAT_012", "short", "sentence", "The sum of the interior angles of a triangle is always 180°.", ["formula", "units"], ["180°"], [], []),
    ("MAT_013", "medium", "sentence", "Two lines are parallel if their slopes are equal, meaning m₁ = m₂.", ["formula", "terminology"], ["m₁ = m₂"], [], [{"en": "parallel", "hi": "समानांतर"}, {"en": "slopes", "hi": "ढलान"}]),
    ("MAT_014", "medium", "sentence", "A logarithm answers the question: to what power must the base be raised to produce a given number?", ["terminology"], [], [], [{"en": "logarithm", "hi": "लघुगणक"}]),
    ("MAT_015", "short", "sentence", "The area of a circle is given by A = πr².", ["formula"], ["A = πr²"], [], []),
    ("MAT_016", "short", "sentence", "The perimeter of a rectangle is P = 2(l + w).", ["formula"], ["P = 2(l + w)"], [], []),
    ("MAT_017", "medium", "sentence", "An integer is a whole number that can be positive, negative, or zero.", ["definition"], [], [], [{"en": "integer", "hi": "पूर्णांक"}]),
    ("MAT_018", "medium", "sentence", "Prime numbers are numbers that have only two distinct positive divisors: 1 and themselves.", ["definition"], [], [], [{"en": "prime numbers", "hi": "अभाज्य संख्याएँ"}]),
    ("MAT_019", "short", "sentence", "The sequence 2, 4, 6, 8 is an arithmetic progression.", ["terminology"], [], [], [{"en": "arithmetic progression", "hi": "समांतर श्रेढ़ी"}]),
    ("MAT_020", "short", "sentence", "The union of two sets A and B is denoted by A ∪ B.", ["formula", "terminology"], ["A ∪ B"], [], [{"en": "union", "hi": "सम्मिलन"}, {"en": "sets", "hi": "समुच्चय"}]),
    ("MAT_021", "medium", "sentence", "A geometric progression is a sequence of numbers where each term after the first is found by multiplying the previous one by a fixed, non-zero number called the common ratio.", ["definition"], [], [], [{"en": "geometric progression", "hi": "गुणोत्तर श्रेढ़ी"}]),
    ("MAT_022", "short", "sentence", "The volume of a sphere is (4/3)πr³.", ["formula"], ["(4/3)πr³"], [], [{"en": "volume", "hi": "आयतन"}]),
    ("MAT_023", "medium", "sentence", "In statistics, the median is the middle value in a given list of numbers when they are ordered.", ["definition"], [], [], [{"en": "median", "hi": "माध्यिका"}]),
    ("MAT_024", "short", "sentence", "Standard deviation measures the amount of variation or dispersion of a set of values.", ["definition"], [], [], [{"en": "standard deviation", "hi": "मानक विचलन"}]),
    ("MAT_025", "medium", "explanation", "If f(x) = x², then the first derivative f'(x) is 2x.", ["formula"], ["f(x) = x²", "f'(x)", "2x"], [], []),
    ("MAT_026", "medium", "sentence", "An acute angle is an angle that measures less than 90 degrees.", ["definition"], [], [], [{"en": "acute angle", "hi": "न्यून कोण"}]),
    ("MAT_027", "medium", "sentence", "A vector space is a set that is closed under finite vector addition and scalar multiplication.", ["terminology"], [], [], [{"en": "vector space", "hi": "सदिश समष्टि"}]),
    ("MAT_028", "short", "sentence", "The limits of integration are from a to b.", ["formula"], ["a", "b"], [], [{"en": "limits of integration", "hi": "समाकलन की सीमाएँ"}]),
    ("MAT_029", "short", "sentence", "Let x and y be real numbers.", ["formula"], ["x", "y"], [], [{"en": "real numbers", "hi": "वास्तविक संख्याएँ"}]),
    ("MAT_030", "medium", "sentence", "The determinant of a 2x2 matrix can be calculated as ad - bc.", ["formula", "terminology"], ["2x2", "ad - bc"], [], [{"en": "determinant", "hi": "सारणिक"}, {"en": "matrix", "hi": "आव्यूह", "kn": "ಮಾತೃಕೆ"}])
]

# ================= CHEMISTRY (20 items) =================
chem_items = [
    ("CHE_001", "short", "sentence", "The chemical formula for water is H₂O.", ["formula"], ["H₂O"], [], [{"en": "chemical formula", "hi": "रासायनिक सूत्र", "kn": "ರಾಸಾಯನಿಕ ಸೂತ್ರ"}]),
    ("CHE_002", "short", "sentence", "Carbon dioxide is represented by CO₂.", ["formula"], ["CO₂"], [], []),
    ("CHE_003", "medium", "sentence", "A molecule of water is formed by two hydrogen atoms and one oxygen atom.", ["terminology"], [], [], [{"en": "molecule", "hi": "अणु", "kn": "ಅಣು"}, {"en": "atoms", "hi": "परमाणु", "kn": "ಪರಮಾಣುಗಳು"}]),
    ("CHE_004", "medium", "definition", "An atom consists of a nucleus surrounded by electrons.", ["terminology"], [], [], [{"en": "atom", "hi": "परमाणु", "kn": "ಪರಮಾಣು"}, {"en": "nucleus", "hi": "नाभिक"}, {"en": "electrons", "hi": "इलेक्ट्रॉन"}]),
    ("CHE_005", "medium", "sentence", "In a covalent bond, pairs of electrons are shared between atoms.", ["terminology"], [], [], [{"en": "covalent bond", "hi": "सहसंयोजक बंधन"}]),
    ("CHE_006", "short", "sentence", "Sodium chloride is commonly known as table salt (NaCl).", ["formula"], ["(NaCl)"], [], []),
    ("CHE_007", "long", "paragraph", "A chemical reaction is a process that leads to the chemical transformation of one set of chemical substances to another. Classically, chemical reactions encompass changes that only involve the positions of electrons in the forming and breaking of chemical bonds between atoms.", ["definition"], [], [], [{"en": "chemical reaction", "hi": "रासायनिक अभिक्रिया"}]),
    ("CHE_008", "medium", "sentence", "Acids are substances that can donate a proton (H⁺) to another substance.", ["formula", "terminology"], ["(H⁺)"], [], [{"en": "acids", "hi": "अम्ल"}, {"en": "proton", "hi": "प्रोटॉन"}]),
    ("CHE_009", "short", "sentence", "The pH scale ranges from 0 to 14.", ["terminology"], [], [], [{"en": "pH scale", "hi": "पीएच पैमाना"}]),
    ("CHE_010", "medium", "sentence", "Exothermic reactions release energy in the form of heat or light.", ["definition"], [], [], [{"en": "exothermic reactions", "hi": "ऊष्माक्षेपी अभिक्रियाएँ"}]),
    ("CHE_011", "medium", "sentence", "Endothermic reactions absorb energy from their surroundings.", ["definition"], [], [], [{"en": "endothermic reactions", "hi": "ऊष्माशोषी अभिक्रियाएँ"}]),
    ("CHE_012", "short", "sentence", "Avogadro's number is approximately 6.022 × 10²³.", ["formula"], ["6.022 × 10²³"], [], []),
    ("CHE_013", "medium", "sentence", "Isotopes are variants of a particular chemical element which differ in neutron number.", ["definition"], [], [], [{"en": "isotopes", "hi": "समस्थानिक"}, {"en": "neutron", "hi": "न्यूट्रॉन"}]),
    ("CHE_014", "medium", "sentence", "A catalyst is a substance that increases the rate of a chemical reaction without itself undergoing any permanent chemical change.", ["definition"], [], [], [{"en": "catalyst", "hi": "उत्प्रेरक"}]),
    ("CHE_015", "short", "sentence", "The periodic table organizes elements based on their atomic number.", ["terminology"], [], [], [{"en": "periodic table", "hi": "आवर्त सारणी"}, {"en": "atomic number", "hi": "परमाणु क्रमांक"}]),
    ("CHE_016", "short", "sentence", "Oxidation is the loss of electrons during a reaction by a molecule, atom or ion.", ["definition"], [], [], [{"en": "oxidation", "hi": "ऑक्सीकरण"}]),
    ("CHE_017", "short", "sentence", "Reduction is the gain of electrons.", ["definition"], [], [], [{"en": "reduction", "hi": "अपचयन"}]),
    ("CHE_018", "medium", "sentence", "A mole is defined as the amount of substance that contains as many elementary entities as there are atoms in 12 grams of carbon-12.", ["definition"], [], [], [{"en": "mole", "hi": "मोल"}]),
    ("CHE_019", "medium", "sentence", "Organic chemistry is the study of the structure, properties, composition, reactions, and preparation of carbon-containing compounds.", ["terminology"], [], [], [{"en": "organic chemistry", "hi": "कार्बनिक रसायन"}]),
    ("CHE_020", "short", "sentence", "The molar mass of water is approximately 18.015 g/mol.", ["units"], ["g/mol"], [], [{"en": "molar mass", "hi": "मोलर द्रव्यमान"}])
]

# ================= BIOLOGY (20 items) =================
bio_items = [
    ("BIO_001", "medium", "definition", "Photosynthesis is the process by which green plants use sunlight to synthesize nutrients from carbon dioxide and water.", ["terminology"], [], [], [{"en": "photosynthesis", "hi": "प्रकाश संश्लेषण", "kn": "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆ"}]),
    ("BIO_002", "short", "sentence", "The cell is the basic structural and functional unit of all living organisms.", ["terminology"], [], [], [{"en": "cell", "hi": "कोशिका"}]),
    ("BIO_003", "medium", "sentence", "DNA (Deoxyribonucleic acid) carries the genetic instructions used in growth, development, functioning, and reproduction.", ["technical_term"], [], ["DNA"], [{"en": "genetic", "hi": "आनुवंशिक"}]),
    ("BIO_004", "medium", "sentence", "Mitochondria are known as the powerhouses of the cell because they generate most of the cell's supply of ATP.", ["terminology"], [], ["ATP"], [{"en": "mitochondria", "hi": "माइटोकॉन्ड्रिया"}]),
    ("BIO_005", "short", "sentence", "Osmosis is the spontaneous net movement of solvent molecules through a selectively permeable membrane.", ["definition"], [], [], [{"en": "osmosis", "hi": "परासरण"}]),
    ("BIO_006", "long", "paragraph", "Cellular respiration is a set of metabolic reactions and processes that take place in the cells of organisms to convert biochemical energy from nutrients into adenosine triphosphate (ATP), and then release waste products.", ["definition", "technical_term"], [], ["ATP"], [{"en": "cellular respiration", "hi": "कोशिकीय श्वसन"}]),
    ("BIO_007", "medium", "sentence", "Enzymes are proteins that act as biological catalysts by accelerating chemical reactions.", ["terminology"], [], [], [{"en": "enzymes", "hi": "एंजाइम"}]),
    ("BIO_008", "short", "sentence", "Mitosis is a part of the cell cycle in which replicated chromosomes are separated into two new nuclei.", ["definition"], [], [], [{"en": "mitosis", "hi": "समसूत्री विभाजन"}]),
    ("BIO_009", "short", "sentence", "Meiosis is a special type of cell division of germ cells in sexually-reproducing organisms.", ["definition"], [], [], [{"en": "meiosis", "hi": "अर्धसूत्री विभाजन"}]),
    ("BIO_010", "medium", "sentence", "A gene is a sequence of nucleotides in DNA or RNA that encodes the synthesis of a gene product, either RNA or protein.", ["terminology"], [], ["DNA", "RNA"], [{"en": "gene", "hi": "जीन"}]),
    ("BIO_011", "medium", "explanation", "Natural selection is the differential survival and reproduction of individuals due to differences in phenotype.", ["terminology"], [], [], [{"en": "natural selection", "hi": "प्राकृतिक चयन"}]),
    ("BIO_012", "short", "sentence", "Ecology is the scientific study of interactions among organisms and their biophysical environment.", ["definition"], [], [], [{"en": "ecology", "hi": "पारिस्थितिकी"}]),
    ("BIO_013", "medium", "sentence", "Pathogens are infectious agents such as viruses, bacteria, prions, or fungi that can cause disease in their host.", ["terminology"], [], [], [{"en": "pathogens", "hi": "रोगजनक"}]),
    ("BIO_014", "medium", "sentence", "The nervous system coordinates the actions of an animal and transmits signals to and from different parts of its body.", ["terminology"], [], [], [{"en": "nervous system", "hi": "तंत्रिका तंत्र"}]),
    ("BIO_015", "short", "sentence", "Hemoglobin is the iron-containing oxygen-transport metalloprotein in the red blood cells.", ["terminology"], [], [], [{"en": "hemoglobin", "hi": "हीमोग्लोबिन"}]),
    ("BIO_016", "medium", "sentence", "Antibodies are large, Y-shaped proteins used by the immune system to identify and neutralize foreign objects like pathogenic bacteria and viruses.", ["definition"], [], [], [{"en": "antibodies", "hi": "एंटीबॉडी"}]),
    ("BIO_017", "medium", "sentence", "Homeostasis is the state of steady internal, physical, and chemical conditions maintained by living systems.", ["definition"], [], [], [{"en": "homeostasis", "hi": "समस्थिति"}]),
    ("BIO_018", "short", "sentence", "Chloroplasts are organelles that conduct photosynthesis.", ["terminology"], [], [], [{"en": "chloroplasts", "hi": "हरितलवक"}]),
    ("BIO_019", "short", "sentence", "Mutations are changes in the genetic sequence, and they are a main cause of diversity among organisms.", ["terminology"], [], [], [{"en": "mutations", "hi": "उत्परिवर्तन"}]),
    ("BIO_020", "medium", "sentence", "The food chain describes the linear sequence of organisms through which nutrients and energy pass as one organism eats another.", ["definition"], [], [], [{"en": "food chain", "hi": "खाद्य श्रृंखला"}])
]

# ================= COMPUTER SCIENCE (25 items) =================
cs_items = [
    ("CS_001", "medium", "definition", "An algorithm is a step-by-step procedure for solving a problem.", ["terminology"], [], [], [{"en": "algorithm", "hi": "एल्गोरिदम", "kn": "ಅಲ್ಗಾರಿದಮ್"}]),
    ("CS_002", "short", "sentence", "Python and NumPy are used for matrix multiplication.", ["technical_term"], [], ["Python", "NumPy"], []),
    ("CS_003", "short", "sentence", "TensorFlow is an open-source machine learning framework.", ["technical_term", "terminology"], [], ["TensorFlow"], [{"en": "framework", "hi": "फ्रेमवर्क", "kn": "ಚೌಕಟ್ಟು"}]),
    ("CS_004", "medium", "sentence", "The web page is styled using HTML and CSS.", ["technical_term"], [], ["HTML", "CSS"], []),
    ("CS_005", "medium", "definition", "A database stores and retrieves structured information.", ["terminology"], [], [], [{"en": "database", "hi": "डेटाबेस", "kn": "ದತ್ತಸಂಚಯ"}]),
    ("CS_006", "short", "sentence", "An API acts as an intermediary between two software applications.", ["technical_term"], [], ["API"], []),
    ("CS_007", "medium", "sentence", "A variable is a storage location paired with an associated symbolic name, which contains some known or unknown quantity of information.", ["terminology", "morphology_risk"], [], [], [{"en": "variable", "hi": "चर"}]),
    ("CS_008", "medium", "sentence", "A function is a sequence of program instructions that performs a specific task, packaged as a unit.", ["terminology"], [], [], [{"en": "function", "hi": "फ़ंक्शन"}]),
    ("CS_009", "long", "paragraph", "Object-oriented programming (OOP) is a programming paradigm based on the concept of \"objects\", which can contain data and code: data in the form of fields (often known as attributes or properties), and code, in the form of procedures (often known as methods).", ["terminology", "technical_term"], [], ["OOP"], [{"en": "Object-oriented programming", "hi": "ऑब्जेक्ट-ओरिएंटेड प्रोग्रामिंग"}]),
    ("CS_010", "medium", "sentence", "Recursion occurs when a function calls itself directly or indirectly in its definition.", ["definition"], [], [], [{"en": "recursion", "hi": "पुनरावर्तन"}]),
    ("CS_011", "medium", "sentence", "A compiler is a computer program that translates computer code written in one programming language into another language.", ["definition"], [], [], [{"en": "compiler", "hi": "कंपाइलर"}]),
    ("CS_012", "short", "sentence", "Binary search runs in O(log n) time.", ["formula", "technical_term"], ["O(log n)"], [], [{"en": "Binary search", "hi": "बाइनरी सर्च"}]),
    ("CS_013", "medium", "sentence", "An operating system manages computer hardware, software resources, and provides common services for computer programs.", ["terminology"], [], [], [{"en": "operating system", "hi": "ऑपरेटिंग सिस्टम"}]),
    ("CS_014", "medium", "sentence", "Machine learning is a subset of artificial intelligence that focuses on building systems that learn based on the data they consume.", ["definition"], [], [], [{"en": "Machine learning", "hi": "मशीन लर्निंग"}]),
    ("CS_015", "short", "sentence", "A linked list is a linear collection of data elements whose order is not given by their physical placement in memory.", ["definition"], [], [], [{"en": "linked list", "hi": "लिंक्ड लिस्ट"}]),
    ("CS_016", "short", "sentence", "The CPU (Central Processing Unit) is the primary component of a computer that acts as its brain.", ["technical_term"], [], ["CPU"], []),
    ("CS_017", "medium", "sentence", "Cryptography is the practice and study of techniques for secure communication in the presence of adversarial behavior.", ["definition"], [], [], [{"en": "Cryptography", "hi": "क्रिप्टोग्राफी"}]),
    ("CS_018", "medium", "sentence", "A hash table uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found.", ["terminology"], [], [], [{"en": "hash table", "hi": "हैश टेबल"}]),
    ("CS_019", "short", "sentence", "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power.", ["definition"], [], [], [{"en": "Cloud computing", "hi": "क्लाउड कंप्यूटिंग"}]),
    ("CS_020", "medium", "sentence", "A boolean data type can only take one of two possible values: true or false.", ["technical_term"], [], ["true", "false"], [{"en": "boolean", "hi": "बूलियन"}]),
    ("CS_021", "medium", "sentence", "Garbage collection is a form of automatic memory management used by some programming languages.", ["terminology"], [], [], [{"en": "Garbage collection", "hi": "गार्बेज कलेक्शन"}]),
    ("CS_022", "short", "sentence", "Polymorphism is the provision of a single interface to entities of different types.", ["definition"], [], [], [{"en": "Polymorphism", "hi": "बहुरूपता"}]),
    ("CS_023", "medium", "sentence", "An IP address is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol.", ["technical_term"], [], ["IP"], []),
    ("CS_024", "medium", "sentence", "Deep learning architectures such as deep neural networks have been applied to fields including computer vision and natural language processing.", ["terminology"], [], [], [{"en": "Deep learning", "hi": "डीप लर्निंग"}]),
    ("CS_025", "short", "sentence", "Git is a distributed version-control system for tracking changes in source code.", ["technical_term"], [], ["Git"], [])
]


for category_items, domain in [(physics_items, "Physics"), (math_items, "Mathematics"), (chem_items, "Chemistry"), (bio_items, "Biology"), (cs_items, "Computer Science")]:
    for item in category_items:
        uid, diff, ctype, src, tags, formulas, tech, terms = item
        dataset.append({
            "id": uid,
            "domain": domain,
            "difficulty": diff,
            "content_type": ctype,
            "source_en": src,
            "risk_tags": tags,
            "formula_tokens": formulas,
            "technical_tokens": tech,
            "terminology_tokens": terms,
            "reference_status": "requires_human_validation"
        })

with open("d:\\SIH\\gate1_benchmark\\gate2_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"Generated {len(dataset)} items in gate2_dataset.json")
