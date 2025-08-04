# UN Annual Reports Gallery (alpha)

A minimal website that displays PDF cover pages of UN organization annual reports in a responsive grid gallery.

## Features

- 📖 Display covers of 51+ UN organization annual reports
- 🎨 Responsive grid layout that adapts to screen size
- 🔗 Direct links to official report pages
- ⚡ Fast loading with optimized images
- 📱 Mobile-friendly design

## Setup

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Extract PDF covers:**

   The gallery needs cover images for each PDF. You have several options:

   **Option A: Automatic extraction (requires ImageMagick)**

   ```bash
   # Install ImageMagick
   brew install imagemagick  # macOS
   # or
   sudo apt-get install imagemagick  # Ubuntu

   # Run extraction script
   ./scripts/extract-covers.sh
   ```

   **Option B: Manual extraction**

   - Open each PDF in Preview/Adobe Reader
   - Export first page as JPG (600x800px recommended)
   - Place in `public/covers/` with names from `data/reports.json`

   **Option C: View filename mapping**

   ```bash
   npm run cover-instructions
   ```

3. **Run the development server:**

   ```bash
   npm run dev
   ```

4. **Open [http://localhost:3000](http://localhost:3000)** in your browser

## Project Structure

```
├── app/
│   ├── page.tsx          # Main gallery page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/
│   └── ReportsGallery.tsx # Gallery grid component
├── data/
│   └── reports.json      # Report metadata
├── docs/                 # PDF files
├── public/
│   └── covers/           # Cover images (you need to add these)
├── scripts/
│   ├── extract-covers.sh # Bash script to extract covers
│   └── cover-instructions.js # Shows required filenames
└── types/
    └── report.ts         # TypeScript types
```

## Data Structure

Each report in `data/reports.json` contains:

```json
{
  "id": "unique-id",
  "name": "Short Name",
  "fullName": "Full Organization Name",
  "year": "2024",
  "filename": "Original_PDF_Name.pdf",
  "coverImage": "cover-image-name.jpg",
  "website": "https://organization.org/",
  "reportUrl": "https://link-to-report-page.org/"
}
```

## Adding New Reports

1. Add the PDF to the `docs/` folder
2. Add an entry to `data/reports.json`
3. Extract/add the cover image to `public/covers/`
4. Update the website and reportUrl with official links

## Performance

- Uses Next.js Image component for optimized loading
- Responsive images with multiple sizes
- Lazy loading for images below the fold
- Minimal CSS for fast rendering

## Deployment

```bash
npm run build
npm start
```

## Fixes

- make sure to replace img tags with next.js optimized tags again once deployed to server and not static GitHub page
