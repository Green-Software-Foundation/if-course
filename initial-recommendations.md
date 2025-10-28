# Audit Report: Impact Framework Course Material

## Overview

This document contains the results of a comprehensive audit of the Impact Framework educational course material (files 1.quickstart.md through 10.next-steps.md) conducted against the official Impact Framework documentation and repository (https://if.greensoftware.foundation and https://github.com/Green-Software-Foundation/if).

**Audit Date**: 2025-10-28
**IF Version Reviewed Against**: v1.1.0 (Latest as of July 21, 2024)
**Total Issues Identified**: 14

---

## CRITICAL ISSUES (Must Fix)

### 1. if-viz Command Does Not Exist
**File**: `1.quickstart.md`
**Lines**: 101-109

**Issue**: The course instructs users to run `if-viz --manifest web.out.yml`, but this command **does not exist** in the current IF CLI toolset.

**Current State**: The official CLI tools are:
- `if-run` (main execution)
- `if-diff` (compare files)
- `if-env` (environment setup)
- `if-check` (verify outputs)
- `if-csv` (export to CSV)
- `if-merge` (combine files)
- `if-api` (HTTP server)

**Evidence**: The visualizer exists at https://viz.if.greensoftware.foundation but appears to be a web-based tool, not a CLI command.

**Suggested Fix**:
Replace the `if-viz` instruction with current best practice. The visualizer likely requires:
1. Hosting the output file on GitHub or a web server
2. Navigating to https://viz.if.greensoftware.foundation
3. Providing the URL to your hosted file

**Recommendation**: Verify the current visualizer workflow and update the entire "View in the Visualizer" section accordingly.

---

### 2. Incomplete TODOs Blocking Student Progress

**File**: `1.quickstart.md`
- **Line 57**: `#TODO` - Missing download link for sample manifest file
- **Line 92**: `TODO` - Missing month information for carbon emissions
- **Line 181**: `TODO - FIX BELOW MESS` - Section about finding model plugins needs cleanup

**File**: `3.direct-measurement.md`
- **Line 181**: `TODO - FIX BELOW MESS` - Same as above, appears to be duplicate content

**Impact**: Students cannot complete the quickstart tutorial without the sample manifest file.

**Suggested Fix**:
- Provide a working sample manifest file (web.yml) for download
- Complete the explanatory text
- Clean up the "finding model plugins" section

---

## HIGH PRIORITY ISSUES (Should Fix)

### 3. Package Installation Command Inconsistency
**File**: `1.quickstart.md`
**Line**: 15

**Current Course**: `npm i -g @grnsft/if`
**Official Docs**: `npm install -g @grnsft/if`

**Issue**: While `npm i` works, official documentation uses the full `npm install` command.

**Suggested Fix**: Use `npm install -g @grnsft/if` for consistency with official docs.

---

### 4. Plugin Configuration Ambiguity
**Files**: `3.direct-measurement.md` & `4.proxy-measurement.md`

**Issue**: The course shows `carbon-from-energy` using the `Coefficient` plugin in explanatory text but then uses the `Multiply` plugin in the actual configuration. This creates confusion.

**File 3 (line 290)**: Says "We configured a `Coefficient` model plugin called `carbon-from-energy`"

**File 3 (actual config shown)**: Uses `Multiply` plugin for `carbon-from-energy`

**Suggested Fix**: Clarify that initially you show one approach (Coefficient), then introduce the Multiply approach, or pick one consistent approach throughout.

---

### 5. Incorrect Plugin Reference in Configuration
**File**: `4.proxy-measurement.md`
**Lines**: 202-207

**Issue**: Shows configuration for `carbon-from-energy` using the `Coefficient` plugin method in text, but the config shown is for `Multiply`:

```yaml
carbon-from-energy:
  method: Multiply  # <-- Says Coefficient in text but shows Multiply
  path: "builtin"
  config:
    input-parameters:
      - energy
      - carbon-intensity
    output-parameter: carbon
```

**Suggested Fix**: Make text and code consistent.

---

## MEDIUM PRIORITY ISSUES

### 6. Hardcoded Absolute File Path
**File**: `6b.sci-walkthrough-mi-operational-energy.md`
**Lines**: 161, 238

**Issue**: Contains hardcoded absolute path:
```yaml
filepath: /Users/jawache/Development/gsf/if-course/src/cloud-metdata-azure-instances.csv
```

**Problem**: This path won't work for students. The file `cloud-metdata-azure-instances.csv` needs to be provided or linked.

**Suggested Fix**:
- Provide the CSV file in the course repository
- Use a relative path like `./data/cloud-metadata-azure-instances.csv`
- Or provide a download link to the GSF maintained dataset

---

### 7. Hardcoded Absolute File Path (Duplicate)
**File**: `6c.sci-walkthrough-mi-oc.md`
**Lines**: 79, 156

**Issue**: Same hardcoded path issue as above.

**Suggested Fix**: Same as issue #6.

---

### 8. Incomplete Documentation Section
**File**: `6d.sci-walkthrough-mi-ec.md`
**Line**: 92

**Issue**: Contains `***** TODO I'M HERE NEED MAPPING DOCS ***`, indicating the section about SciEmbodied plugin with mappings is incomplete.

**Impact**: Students won't know how to configure the embodied carbon plugin correctly.

**Suggested Fix**: Complete the mapping documentation or remove the TODO marker if the section is actually complete.

---

### 9. Confusing Mix of Old and New Content
**File**: `7.time.md`

**Issue**: The file contains two distinct sections:
- Lines 1-22: New, well-formatted content about time-sync feature
- Lines 24-118: Old course material marked with "ORIG COURSE"

**Suggested Fix**: Remove the old content or clearly indicate it's deprecated. The duplication is confusing.

---

### 10. Duplicate Content
**File**: `8.aggregation.md`

**Issue**: Similar to file 7, contains:
- Lines 1-16: New, comprehensive content about aggregation
- Lines 18-52: Old course material with different structure

**Suggested Fix**: Consolidate into single coherent section.

---

## LOW PRIORITY ISSUES (Good to Fix)

### 11. Spelling Error Throughout Multiple Files
**Files**: `6a.sci-walkthrough-ido.md`, `6b.sci-walkthrough-mi-operational-energy.md`, `6c.sci-walkthrough-mi-oc.md`
**Line**: 98 (and throughout)

**Issue**: "impact dependancy tree" - should be "impact **dependency** tree"

**Suggested Fix**: Global search and replace "dependancy" → "dependency"

---

### 12. Confusing Line Numbers in Comment
**File**: `3.direct-measurement.md`
**Lines**: 183-185

**Issue**: The comment markers `# <1>`, `# <2>`, etc. in the YAML example don't clearly map to the explanations below. Line 206 references `<7>` but should be `<6>`.

**Suggested Fix**: Verify all numbered references match correctly.

---

### 13. Missing Diagrams
**File**: `6b.sci-walkthrough-mi-operational-energy.md`
**Lines**: 78, 120

**Issue**: Contains `**TODO - DIAGRAM**` and `**TODO - IMAGE**` markers.

**Impact**: Visual aids would greatly help students understand power curves.

**Suggested Fix**: Add the diagrams or remove the TODO markers.

---

### 14. Missing Version Information
**All Files**

**Issue**: The course doesn't mention which version of IF it's targeting.

**Current Version**: v1.1.0 (July 21, 2024)

**Major Changes Since v1.0.0**:
- API server capability added (`if-api`)
- Docker/Kubernetes support
- CSV import functionality

**Breaking Changes from v0.x**:
- `global-config` renamed to `config`
- `override params` flag removed from if-run

**Suggested Fix**: Add a version notice at the beginning stating the course targets IF v1.1.0+

---

## CONTENT VERIFICATION NEEDED

These items need verification against current IF behavior:

1. **Pipeline structure** - Verify `pipeline: compute:` is still the correct syntax
2. **Plugin path** - Confirm `path: "builtin"` is still correct for builtin plugins
3. **Interpolation plugin** - Verify the Interpolation plugin configuration (6b.sci-walkthrough-mi-operational-energy.md:131-140)
4. **SciEmbodied plugin** - Verify current configuration requirements
5. **Aggregation syntax** - Verify aggregation configuration in manifest files

---

## SUMMARY STATISTICS

| Priority Level | Count | Percentage |
|---------------|-------|------------|
| Critical      | 2     | 14%        |
| High          | 3     | 21%        |
| Medium        | 5     | 36%        |
| Low           | 4     | 29%        |
| **Total**     | **14**| **100%**   |

### Issues by File

| File | Issue Count |
|------|-------------|
| 1.quickstart.md | 4 |
| 3.direct-measurement.md | 2 |
| 4.proxy-measurement.md | 2 |
| 6a.sci-walkthrough-ido.md | 1 |
| 6b.sci-walkthrough-mi-operational-energy.md | 3 |
| 6c.sci-walkthrough-mi-oc.md | 2 |
| 6d.sci-walkthrough-mi-ec.md | 1 |
| 7.time.md | 1 |
| 8.aggregation.md | 1 |
| All files | 1 |

---

## RECOMMENDED ACTION PLAN

### Phase 1: Critical Fixes (Week 1)
1. Research and document the current visualizer workflow
2. Create and host the sample web.yml manifest file
3. Update 1.quickstart.md with correct visualizer instructions
4. Complete all blocking TODO sections

### Phase 2: High Priority Fixes (Week 1-2)
1. Resolve plugin configuration inconsistencies
2. Choose consistent approach (Multiply vs Coefficient) throughout
3. Update installation command to match official docs

### Phase 3: Medium Priority Fixes (Week 2-3)
1. Fix all hardcoded paths
2. Provide or link to required CSV files
3. Complete the SciEmbodied mapping documentation
4. Consolidate duplicate content in files 7 and 8

### Phase 4: Low Priority Fixes (Week 3-4)
1. Global spell-check (dependancy → dependency)
2. Add version information to course introduction
3. Fix numbered reference mismatches
4. Add missing diagrams or remove TODO markers

### Phase 5: Verification (Week 4)
1. Test all manifest examples against IF v1.1.0
2. Verify plugin configurations
3. Complete student walkthrough testing

---

## TESTING RECOMMENDATIONS

Before considering the course updated, recommend:

1. **Manual Testing**: Have a fresh user follow the quickstart guide end-to-end
2. **Manifest Validation**: Run all example manifests through `if-run` to ensure they execute
3. **Version Testing**: Verify examples work with IF v1.1.0+
4. **Link Checking**: Verify all external links are functional
5. **File Availability**: Ensure all referenced files are accessible

---

## POSITIVE FINDINGS

Despite the issues identified, the course material has several strengths:

1. **Comprehensive Coverage**: Covers the full IDOMI methodology thoroughly
2. **Progressive Learning**: Good progression from simple to complex examples
3. **Real-World Examples**: Uses practical examples like the GSF website
4. **Clear Structure**: Well-organized with numbered modules
5. **Good Pedagogy**: Includes quizzes and exercises
6. **Detailed Walkthroughs**: Step-by-step SCI calculation examples are excellent

---

## CONCLUSION

The course material is fundamentally sound but requires updates to align with the current IF v1.1.0 implementation. The most critical issue is the non-existent `if-viz` command which would prevent students from completing the quickstart. Once the critical and high-priority issues are addressed, this will be an excellent educational resource for the Impact Framework.

**Estimated Total Effort**: 2-4 weeks for complete remediation

**Recommended Priority**: Start with Critical and High Priority issues for immediate usability, then address Medium and Low Priority issues for polish and completeness.
