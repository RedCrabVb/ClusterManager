

export interface ITreeView {
    name: string
    type: 'directory' | 'file'
    children?: ITreeView[]
} 