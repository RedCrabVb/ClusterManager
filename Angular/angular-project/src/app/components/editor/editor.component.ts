import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core'

declare var CodeMirror: any

@Component({
    selector: 'editor',
    template: `
    <textarea #editor style="height: 100%; width: 100%">
    </textarea>
`,
    styleUrls: [
        '../../../../node_modules/codemirror/lib/codemirror.css'
    ]
})

export class EditorComponent implements AfterViewInit, OnInit {
    @ViewChild('editor') editor: any;
    @Input() content: string
    editorMirror: any;

    constructor() {
        console.log(this.content)
        console.log(this.content)
        console.log(this.content)
        console.log(this.content)
        console.log(this.content)
    }

    ngOnInit() {
        console.log(this.editor);
    }

    ngAfterViewInit(): void {
        console.log(this.editor.nativeElement)
        this.editorMirror = new CodeMirror.fromTextArea(this.editor.nativeElement, {
            lineNumbers: true,
            lineWrapping: true,
            styleActiveLine: true,
            autoRefresh: true,
            mode: 'text',
            theme: "monokai",
        }
        );
        console.log(this.editorMirror)

        this.editorMirror.on('change', (editor: any) => {
            console.log(this.editorMirror.getDoc().getValue());
        });

        this.editorMirror.setValue('asdf')

        let edRef = this.editorMirror
        console.log(this.content)
        console.log(this.content)
        console.log(this.content)
        console.log(this.content)
        console.log(this.content)
        // setTimeout(function () {
        //     edRef.refresh()
        //     console.log(this.content)
        //     console.log('ef refresh')
        // }, 1);

    }

}