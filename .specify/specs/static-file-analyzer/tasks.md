# Tasks: Static File Analyzer

**Input**: Design documents from `/specs/static-file-analyzer/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/
- [x] T002 Create requirements.txt with Flask, openpyxl, xlrd, pandas, tabula-py, pytest
- [x] T003 [P] Create config.py in src/config.py for Flask configuration
- [x] T004 [P] Create base directory structure in src/templates/ and src/static/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create base app.py in src/app.py with Flask initialization
- [x] T006 [P] Implement file validator service in src/services/validator.py
- [x] T007 [P] Implement base file parser skeleton in src/services/file_parser.py
- [x] T008 [P] Implement statistics service skeleton in src/services/statistics.py
- [x] T009 [P] Create base template in src/templates/base.html with Bootstrap 5
- [x] T010 [P] Setup test environment in tests/conftest.py
- [x] T011 Configure error handling and logging infrastructure in src/app.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - File Loading by Drag-and-Drop (Priority: P1) 🎯 MVP

**Goal**: User can drag and drop a valid file (.xlsx, .xls, .pdf, .csv) on the dropzone and the file is recognized

**Independent Test**: Drop a valid file on the zone, verify the file name appears and the "Démarrer l'analyse" button is visible

### Tests for User Story 1 (OPTIONAL)

- [x] T012 [P] [US1] Unit test for file validator in tests/unit/test_validator.py
- [x] T013 [P] [US1] Integration test for file upload in tests/integration/test_app.py

### Implementation for User Story 1

- [x] T014 [P] [US1] Create FichierAnalyse entity in src/models/fichier_analyse.py
- [x] T015 [US1] Implement file dropzone UI in src/templates/index.html
- [x] T016 [US1] Implement JavaScript drag-drop logic in src/static/js/app.js
- [x] T017 [US1] Implement POST /upload route in src/app.py
- [x] T018 [US1] Add file validation on upload in src/app.py
- [x] T019 [US1] Add CSS styles for dropzone in src/static/css/styles.css

**Checkpoint**: At this point, User Story 1 should be fully functional - users can drop files and see them loaded

---

## Phase 4: User Story 2 - Analysis Launch and Results Display (Priority: P1)

**Goal**: User can click "Démarrer l'analyse", see a popup, and view the global statistics

**Independent Test**: Click the start button, wait for analysis, verify the 4 statistics are displayed with colors

### Tests for User Story 2 (OPTIONAL)

- [ ] T020 [P] [US2] Unit test for statistics service in tests/unit/test_statistics.py
- [ ] T021 [P] [US2] Unit test for file parser in tests/unit/test_file_parser.py

### Implementation for User Story 2

- [ ] T022 [P] [US2] Create StatistiquesGlobales entity in src/models/statistiques_globales.py
- [ ] T023 [US2] Implement .xlsx parser in src/services/file_parser.py
- [ ] T024 [US2] Implement .xls parser in src/services/file_parser.py
- [ ] T025 [US2] Implement .csv parser in src/services/file_parser.py
- [ ] T026 [US2] Implement .pdf parser in src/services/file_parser.py
- [ ] T027 [US2] Implement statistics calculation in src/services/statistics.py
- [ ] T028 [US2] Implement POST /analyze route in src/app.py
- [ ] T029 [US2] Create results template in src/templates/results.html
- [ ] T030 [US2] Add popup notification logic in src/static/js/app.js
- [ ] T031 [US2] Add color thresholds logic in src/static/js/app.js

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Multi-Format Support and Error Handling (Priority: P2)

**Goal**: System handles all supported formats and rejects invalid files with clear error messages

**Independent Test**: Upload files in different formats (.xlsx, .xls, .pdf, .csv), verify all work. Upload an invalid file (.docx), verify error message.

### Tests for User Story 3 (OPTIONAL)

- [ ] T032 [P] [US3] Integration test for all formats in tests/integration/test_formats.py
- [ ] T033 [P] [US3] Integration test for invalid format in tests/integration/test_errors.py

### Implementation for User Story 3

- [ ] T034 [US3] Add error state to ZoneDepot in src/models/fichier_analyse.py
- [ ] T035 [US3] Implement error response handler in src/app.py
- [ ] T036 [US3] Add error message UI in src/templates/index.html
- [ ] T037 [US3] Add file size validation in src/services/validator.py
- [ ] T038 [US3] Add user-friendly error messages in src/static/js/app.js

**Checkpoint**: All supported formats work, invalid formats are rejected

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T039 [P] Add professional CSS styling in src/static/css/styles.css
- [ ] T040 [P] Add responsive design for mobile in src/static/css/styles.css
- [ ] T041 Add documentation in src/README.md
- [ ] T042 [P] Add unit tests for edge cases in tests/unit/test_edge_cases.py
- [ ] T043 Run quickstart.md validation scenarios
- [ ] T044 Add accessibility attributes (ARIA) in src/templates/index.html
- [ ] T045 Performance testing with 10k rows file

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Depends on US1 for UI integration
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Can integrate with US1/US2

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
