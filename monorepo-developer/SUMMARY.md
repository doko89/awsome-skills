# Monorepo Developer Skill - Summary

## 📦 Skill Overview

**monorepo-developer** adalah skill komprehensif untuk membangun aplikasi fullstack modern menggunakan:
- **Bun** - Runtime JavaScript yang cepat
- **Hono** - Web framework ringan untuk backend
- **React 19** - Frontend framework terbaru
- **shadcn/ui** - Komponen UI yang indah
- **TypeScript** - Type safety di seluruh stack
- **Tailwind CSS** - Utility-first CSS framework

## 📁 Struktur Skill

```
monorepo-developer/
├── SKILL.md                          # Dokumentasi skill utama
├── README.md                         # Quick start guide
├── SUMMARY.md                        # Comprehensive summary
├── LICENSE                           # MIT License
├── scripts/                          # Python scripts untuk automation (7 scripts)
│   ├── init_project.py              # Inisialisasi monorepo baru
│   ├── generate_package.py          # Generate package baru
│   ├── generate_component.py        # Generate React components
│   ├── generate_hook.py             # Generate custom hooks
│   ├── generate_page.py             # Generate React pages
│   ├── add_component.py             # Tambah shadcn/ui components
│   └── validate_skill.py            # Validasi struktur skill
├── references/                       # Dokumentasi referensi (4 files)
│   ├── bun_hono_setup.md            # Setup Bun + Hono
│   ├── monorepo_best_practices.md   # Best practices monorepo
│   ├── react_shadcn_best_practices.md # Best practices React + shadcn
│   └── react_code_generation.md     # React code generation guide
├── examples/                         # Contoh penggunaan
│   ├── quick_start.md               # Quick start guide
│   └── advanced_setup.md            # Setup advanced
└── assets/                           # Folder untuk assets (kosong)
```

## 🚀 Scripts

### 1. init_project.py
**Fungsi**: Menginisialisasi monorepo baru dengan struktur lengkap

**Penggunaan**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/init_project.py my-monorepo [--skip-git] [--skip-install]
```

**Membuat**:
- ✅ Bun workspace configuration
- ✅ Backend package dengan Hono
- ✅ Frontend package dengan React + shadcn/ui
- ✅ Shared package untuk types dan utilities
- ✅ TypeScript configuration
- ✅ Development scripts
- ✅ Git repository (optional)

### 2. generate_package.py
**Fungsi**: Generate package baru dalam monorepo

**Penggunaan**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py <package-name> --type <type> [--project-path <path>]
```

**Package Types**:
- `backend` - Hono backend service
- `frontend` - React frontend application
- `library` - Shared library package

**Contoh**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py api-service --type backend
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py admin-panel --type frontend
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py utils --type library
```

### 3. add_component.py
**Fungsi**: Tambah shadcn/ui components ke frontend packages

**Penggunaan**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/add_component.py [components...] [--package <name>] [--project-path <path>]
```

**Contoh**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/add_component.py button card dialog
python ~/.claude/skills/monorepo-developer/scripts/add_component.py --preset forms
python ~/.claude/skills/monorepo-developer/scripts/add_component.py --list
```

### 4. generate_component.py
**Fungsi**: Generate React components dengan berbagai template

**Penggunaan**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py <component-name> [--type <type>] [--directory <dir>] [--package <name>]
```

**Component Types**:
- `basic` - Basic component dengan props interface
- `children` - Component dengan children prop
- `state` - Component dengan useState hook
- `form` - Form component dengan validation
- `card` - Card component dengan shadcn/ui
- `list` - List component dengan rendering
- `modal` - Modal/Dialog component

**Contoh**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserCard --type card
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py LoginForm --type form
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserList --type list --directory features/users
```

### 5. generate_hook.py
**Fungsi**: Generate custom React hooks

**Penggunaan**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py <hook-name> [--type <type>] [--package <name>]
```

**Hook Types**:
- `basic` - Basic hook template
- `fetch` - Data fetching hook
- `local-storage` - localStorage hook
- `debounce` - Debounce hook
- `throttle` - Throttle hook
- `toggle` - Toggle boolean state
- `previous` - usePrevious hook
- `async` - Async operation hook

**Contoh**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useUserData --type fetch
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useLocalStorage --type local-storage
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useDebounce --type debounce
```

### 6. generate_page.py
**Fungsi**: Generate React pages

**Penggunaan**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py <page-name> [--type <type>] [--package <name>]
```

**Page Types**:
- `basic` - Basic page template
- `list` - List page dengan search dan filtering
- `detail` - Detail page dengan back button
- `form` - Form page dengan submission
- `dashboard` - Dashboard dengan stats cards

**Contoh**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py Dashboard --type dashboard
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py UserList --type list
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py UserDetail --type detail
```

### 7. validate_skill.py
**Fungsi**: Validasi struktur skill

**Penggunaan**:
```bash
python ~/.claude/skills/monorepo-developer/scripts/validate_skill.py
```

**Checks**:
- ✅ SKILL.md structure
- ✅ Scripts directory
- ✅ Documentation files
- ✅ References
- ✅ Examples

## 📚 Dokumentasi

### SKILL.md
Dokumentasi utama skill dengan:
- Overview dan features
- Tech stack details
- Project structure
- Scripts documentation
- Usage guidelines
- Best practices
- Troubleshooting

### README.md
Quick start guide dengan:
- Features overview
- Quick start steps
- Project structure
- Scripts reference
- Tech stack
- Development workflow
- Best practices
- Troubleshooting

### References

#### bun_hono_setup.md
- Pengenalan Bun dan Hono
- Bun workspace setup
- Hono backend setup
- Middleware configuration
- Routing patterns
- Environment variables
- Type safety
- Performance tips
- Deployment guide

#### monorepo_best_practices.md
- Workspace structure
- Dependency management
- Code sharing patterns
- Development workflow
- Environment variables
- Version management
- Git workflow
- Performance optimization
- Deployment strategies
- Security best practices

#### react_shadcn_best_practices.md
- Component organization
- Component patterns
- State management dengan Zustand
- Data fetching dengan React Query
- Custom hooks
- Styling dengan Tailwind
- Form handling
- Performance optimization
- Error handling
- Testing patterns

### Examples

#### quick_start.md
Step-by-step guide untuk:
1. Create monorepo
2. Start development
3. Explore structure
4. Add backend routes
5. Add frontend components
6. Create React components
7. Use components in app
8. Generate new packages
9. Build for production
10. Deploy

#### advanced_setup.md
Advanced patterns untuk:
- Multi-service architecture
- Multiple frontend applications
- Shared UI library
- Database integration (Drizzle ORM)
- Authentication (JWT)
- API client library
- Testing strategy
- CI/CD pipeline
- Monitoring dan logging
- Performance monitoring
- Docker deployment
- Kubernetes deployment

## 🎯 Quick Start

### 1. Create Monorepo
```bash
python ~/.claude/skills/monorepo-developer/scripts/init_project.py my-app
cd my-app
```

### 2. Start Development
```bash
bun run dev
```

### 3. Generate Packages
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py api --type backend
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py admin --type frontend
```

### 4. Add Components
```bash
python ~/.claude/skills/monorepo-developer/scripts/add_component.py --preset forms --package frontend
```

## 📊 Tech Stack Versions

- **Bun**: 1.0+
- **Hono**: 4.10.3
- **React**: 19.2.0
- **TypeScript**: 5.9.3
- **Tailwind CSS**: 4.1.16
- **Vite**: 7.1.12
- **React Router**: 7.9.4
- **TanStack Query**: 5.90.5
- **Zustand**: 5.0.8
- **Axios**: 1.12.2

## ✅ Validation Status

Semua checks telah passed:
- ✅ SKILL.md structure
- ✅ Scripts directory
- ✅ Documentation files
- ✅ References
- ✅ Examples

## 🔧 Features

### Project Initialization
- ✅ Bun workspace setup
- ✅ Backend package dengan Hono
- ✅ Frontend package dengan React + shadcn/ui
- ✅ Shared package untuk types
- ✅ TypeScript configuration
- ✅ Development scripts
- ✅ Git initialization

### Package Generation
- ✅ Backend services (Hono)
- ✅ Frontend applications (React)
- ✅ Library packages (shared code)
- ✅ Automatic configuration
- ✅ TypeScript setup

### Component Management
- ✅ Add shadcn/ui components
- ✅ Preset groups (forms, data, overlay, etc.)
- ✅ List available components
- ✅ Package-specific installation

### Validation
- ✅ Skill structure validation
- ✅ File existence checks
- ✅ Documentation validation
- ✅ Script validation

## 🎓 Learning Resources

Skill ini menyediakan:
1. **SKILL.md** - Dokumentasi lengkap
2. **README.md** - Quick start guide
3. **3 Reference files** - Detailed guides
4. **2 Example files** - Practical examples
5. **4 Python scripts** - Automation tools

## 🚀 Use Cases

Skill ini cocok untuk:
- ✅ Building fullstack applications
- ✅ Creating monorepo projects
- ✅ Rapid prototyping
- ✅ Team collaboration
- ✅ Microservices architecture
- ✅ Multi-app projects
- ✅ Shared component libraries

## 📝 Next Steps

1. **Initialize Project**: `python ~/.claude/skills/monorepo-developer/scripts/init_project.py my-app`
2. **Explore Structure**: `cd my-app && ls -la`
3. **Start Development**: `bun run dev`
4. **Generate Packages**: `python ~/.claude/skills/monorepo-developer/scripts/generate_package.py ...`
5. **Add Components**: `python ~/.claude/skills/monorepo-developer/scripts/add_component.py ...`
6. **Build & Deploy**: `bun run build`

## 📞 Support

Untuk bantuan:
1. Baca SKILL.md untuk dokumentasi lengkap
2. Lihat examples/ untuk contoh praktis
3. Baca references/ untuk detailed guides
4. Jalankan validate_skill.py untuk troubleshooting

---

**Created**: 2024
**License**: MIT
**Version**: 1.0.0
