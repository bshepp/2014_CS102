# Contributing to Claude Web Deployment Templates

Thank you for helping improve these battle-tested deployment templates! Every contribution helps Claude Code instances deploy faster and more reliably.

## 🤝 How to Contribute

### 1. Found a New Issue?

**Document it using the established format:**

#### For AI_AGENT_CI_CHECKLIST.md
```markdown
### X. [Issue Category Name]

**Problem**: [Brief description of the issue]

**Check Steps:**
1. [Specific verification steps]
2. [Commands to run]
3. [Files to check]

**Common patterns to fix:**
```[language]
# WRONG
[incorrect example]

# CORRECT  
[corrected example]
```

**Verification:**
- [ ] [Checklist item 1]
- [ ] [Checklist item 2]
```

#### For LESSONS_LEARNED.md
```markdown
### X. [Problem Title]
**Problem**: [Description of what went wrong]
**Solution**: [How it was fixed]
**Lesson**: [Key takeaway for future deployments]
```

### 2. Fixed a Template Issue?

1. **Update the relevant template files**
2. **Test your fix** with a real deployment
3. **Document the change** in the appropriate file
4. **Update version references** if needed
5. **Submit a Pull Request** with clear description

### 3. Improved CI/CD Workflow?

**Priority: Update validate.yml first**, then document:

1. **Test thoroughly** - Deploy to real environment
2. **Update validate.yml** with working implementation  
3. **Document in AI_AGENT_CI_CHECKLIST.md** - Add systematic debugging steps
4. **Add to LESSONS_LEARNED.md** - Explain why the change was needed
5. **Update README.md** - Add to "Proven Solutions" list if major fix

## 📋 Contribution Checklist

### Before Submitting PR:
- [ ] **No secrets** - Scan your changes for API keys, tokens, passwords
- [ ] **Templates work** - Test with fresh project deployment
- [ ] **Documentation updated** - Relevant files reflect your changes
- [ ] **Cross-references accurate** - Links between documents work
- [ ] **Placeholders proper** - Use `[CUSTOMIZE]` format consistently

### Security Requirements:
- [ ] **No hardcoded credentials** in any template
- [ ] **No specific AWS account IDs** or resource identifiers
- [ ] **No internal URLs** or private network references
- [ ] **Example credentials clearly fake** (e.g., `sk-1234567890abcdef`)

### Quality Standards:
- [ ] **Commands tested** - All bash/CLI commands work as documented
- [ ] **Syntax validated** - YAML, markdown, code blocks are correct
- [ ] **Links functional** - All internal references work
- [ ] **Consistent formatting** - Follow existing style patterns

## 🎯 High-Value Contributions

### Most Needed Improvements:
1. **New deployment patterns** - Support for additional platforms (Vercel, Railway, etc.)
2. **Security enhancements** - Additional scanning tools and configurations
3. **Performance optimizations** - Faster CI/CD workflows
4. **Accessibility improvements** - Enhanced a11y testing and patterns
5. **Monitoring integration** - Application performance monitoring templates

### Documentation Priorities:
1. **Real-world examples** - More implementation case studies
2. **Troubleshooting guides** - Common error messages and fixes
3. **Architecture decisions** - Why specific choices were made
4. **Tool comparisons** - When to use different approaches

## 🔄 Review Process

### Pull Request Review:
1. **Automated testing** - GitHub Actions validate changes
2. **Template testing** - Maintainers test with real deployments  
3. **Security review** - Manual scan for sensitive information
4. **Documentation check** - Ensure consistency across files
5. **Community feedback** - Other Claude instances may test changes

### Approval Criteria:
- ✅ **Solves real problem** that multiple deployments would face
- ✅ **Tested implementation** - Works in production environment
- ✅ **Clear documentation** - Other Claude instances can follow it
- ✅ **No security risks** - No credentials or sensitive data
- ✅ **Consistent style** - Matches existing template patterns

## 🚀 Types of Contributions

### Code Templates
- **CI/CD workflow improvements** (validate.yml)
- **Configuration file templates** (amplify.yml, etc.)
- **Docker configurations** (distroless patterns, etc.)
- **Security scanning setups** (new tools, better configs)

### Documentation
- **New problem solutions** (AI_AGENT_CI_CHECKLIST.md)
- **Deployment lessons** (LESSONS_LEARNED.md)  
- **Architecture guides** (new deployment patterns)
- **Troubleshooting help** (common error fixes)

### Examples
- **Real implementations** showing template usage
- **Migration guides** from other platforms
- **Integration patterns** with different services
- **Performance optimization case studies**

## 🏷 Issue Labels

When creating issues, use these labels:

- **`bug`** - Something broken in existing templates
- **`enhancement`** - Improvement to existing functionality  
- **`new-template`** - Request for new template type
- **`documentation`** - Docs need improvement
- **`security`** - Security-related issue or enhancement
- **`ci-cd`** - CI/CD workflow improvements
- **`aws`** - AWS-specific improvements
- **`accessibility`** - A11y testing and compliance
- **`performance`** - Speed and optimization improvements

## 💡 Getting Started

### For New Contributors:
1. **Read the templates** - Understand current patterns
2. **Try a deployment** - Use templates for real project  
3. **Find pain points** - What could be improved?
4. **Start small** - Fix documentation or add examples
5. **Build up** - Contribute larger improvements over time

### For Claude Code Instances:
1. **Document as you go** - Note issues during deployments
2. **Share solutions** - Help other Claude instances avoid same problems
3. **Test thoroughly** - Ensure your fixes work reliably
4. **Think systematically** - How does this fit into overall template ecosystem?

## 📞 Getting Help

### Questions?
- **Check existing docs first** - README.md, LESSONS_LEARNED.md
- **Search issues** - Problem might already be documented
- **Create discussion** - For questions about best approaches
- **Tag maintainers** - For urgent issues or clarifications

### Maintainer Contact:
- **Primary**: Dark Forest Labs Claude instances
- **GitHub**: @darkforest-labs organization
- **Response time**: Usually within 24-48 hours

## 🙏 Recognition

Contributors will be recognized:
- **CHANGELOG.md** - Major contributions documented
- **README.md** - Success stories section
- **Git history** - Permanent record of improvements
- **Issue credits** - Referenced in related documentation

---

**Remember**: Every contribution, no matter how small, helps Claude Code instances deploy faster and more reliably. Your improvements will save tokens and time for the entire Claude ecosystem! 🚀

*Thank you for making web deployment better for AI agents everywhere.*