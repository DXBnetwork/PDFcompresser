// netlify/functions/split-pdf.js
const { PDFDocument } = require('pdf-lib')
const JSZip = require('jszip')
const Busboy = require('busboy')

exports.handler = async (event, context) => {
  return new Promise((resolve, reject) => {
    const busboy = Busboy({ headers: event.headers })
    let fileBuffer = Buffer.alloc(0)
    let maxSizeMB = 10

    busboy.on('field', (name, val) => {
      if (name === 'max_size') maxSizeMB = parseInt(val,10)
    })

    busboy.on('file', (name, file) => {
      file.on('data', data => {
        fileBuffer = Buffer.concat([ fileBuffer, data ])
      })
    })

    busboy.on('finish', async () => {
      try {
        const srcDoc = await PDFDocument.load(fileBuffer)
        const maxBytes = maxSizeMB * 1024 * 1024
        const total = srcDoc.getPageCount()
        let chunkPages = [], idx = 1, parts = []

        for (let i = 0; i < total; i++) {
          const testPages = chunkPages.concat(i)
          const testDoc = await PDFDocument.create()
          const [p] = await testDoc.copyPages(srcDoc, testPages)
          testDoc.addPage(p)
          const bytes = await testDoc.save()
          if (bytes.byteLength <= maxBytes) {
            chunkPages = testPages
          } else {
            if (!chunkPages.length) chunkPages = testPages
            const outDoc = await PDFDocument.create()
            const copied = await outDoc.copyPages(srcDoc, chunkPages)
            copied.forEach(p=>outDoc.addPage(p))
            parts.push({ name:`part_${idx}.pdf`, data: Buffer.from(await outDoc.save()) })
            idx++; chunkPages = [i]
          }
        }

        if (chunkPages.length) {
          const outDoc = await PDFDocument.create()
          const copied = await outDoc.copyPages(srcDoc, chunkPages)
          copied.forEach(p=>outDoc.addPage(p))
          parts.push({ name:`part_${idx}.pdf`, data: Buffer.from(await outDoc.save()) })
        }

        const zip = new JSZip()
        parts.forEach(p=> zip.file(p.name, p.data))
        const zipBuf = await zip.generateAsync({ type:'nodebuffer' })

        resolve({
          statusCode: 200,
          headers: {
            'Content-Type': 'application/zip',
            'Content-Disposition': 'attachment; filename="pdf_parts.zip"'
          },
          body: zipBuf.toString('base64'),
          isBase64Encoded: true
        })
      } catch (err) {
        console.error(err)
        resolve({ statusCode: 500, body: 'Split failed' })
      }
    })

    busboy.end(Buffer.from(event.body, event.isBase64Encoded ? 'base64' : 'utf8'))
  })
}
