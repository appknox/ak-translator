export interface TranslationMessage {
  type: string
  language?: string
  translated_text?: TranslationResult
  original_text?: string
  completed_count?: number
  total_count?: number
  progress?: string
  error?: string
  job_id?: string
}

export interface TranslationResult {
  is_json: boolean
  is_string: boolean
  original_input: string
  target_language: string
  final_translation: string | object
  translation_rating: number
  review_decision: string
  review_reasoning: string
  iterations: number
}

export interface WebSocketCallbacks {
  onConnect?: () => void
  onDisconnect?: () => void
  onLanguageCompleted?: (result: TranslationResult) => void
  onAllCompleted?: (translations: Record<string, string>) => void
  onProgress?: (language: string, message: string) => void
  onError?: (error: string, language?: string) => void
}

// src/services/websocket.ts
class TranslationWebSocket {
  private ws: WebSocket | null = null
  private clientId: string
  private isConnected: boolean = false
  private translations: Map<string, TranslationResult> = new Map()
  private wsUrl: string

  // Event callbacks
  public onConnect?: () => void
  public onDisconnect?: () => void
  public onLanguageCompleted?: (result: TranslationResult) => void
  public onAllCompleted?: (translations: Map<string, TranslationResult>) => void
  public onProgress?: (language: string, message: string) => void
  public onTranslationError?: (error: string, language?: string) => void
  public onConnectionError?: (error: string) => void

  constructor() {
    this.clientId = this.generateClientId()
    this.wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
  }

  private generateClientId(): string {
    return 'client_' + Date.now() + '_' + Math.random().toString(36).substring(2, 9)
  }

  public connect(): void {
    try {
      this.ws = new WebSocket(`${this.wsUrl}/ws/${this.clientId}`)

      this.ws.onopen = () => {
        this.isConnected = true
        this.onConnect?.()
        console.log('WebSocket connected')
      }

      this.ws.onmessage = event => {
        const message: TranslationMessage = JSON.parse(event.data)
        this.handleMessage(message)
      }

      this.ws.onclose = () => {
        this.isConnected = false
        console.log('WebSocket disconnected')
        this.onDisconnect?.()
      }

      this.ws.onerror = error => {
        console.error('WebSocket error:', error)
        this.onConnectionError?.('Connection error')
      }
    } catch (error) {
      console.error('Failed to connect:', error)
      this.onConnectionError?.('Failed to connect')
    }
  }

  private handleMessage(message: TranslationMessage): void {
    const { type } = message

    switch (type) {
      case 'language_translation_completed':
        if (message.language && message.translated_text) {
          this.translations.set(message.language, message.translated_text)
          this.onLanguageCompleted?.(message.translated_text)
        }

        break

      case 'language_translation_started':
        if (message.language && message.progress) {
          this.onProgress?.(message.language, message.progress)
        }

        break

      case 'multi_translation_completed':
        this.onAllCompleted?.(this.translations)
        break

      case 'language_translation_failed':
      case 'translation_error':
        this.onTranslationError?.(message.error || 'Unknown error', message.language)
        break
    }
  }

  private regenerateClientId(): void {
    this.clientId = this.generateClientId()
  }

  public translateMultiple(text: string): void {
    if (!this.isConnected) {
      throw new Error('WebSocket not connected')
    }

    this.translations.clear()

    const message = {
      type: 'translate_multi',
      text: text,
      job_id: `job_${Date.now()}`,
    }

    this.ws?.send(JSON.stringify(message))
  }

  public disconnect(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
      this.isConnected = false
    }
  }

  public reconnect(): void {
    if (this.isConnected) {
      this.disconnect()
    }

    this.regenerateClientId()
    this.connect()
  }

  public getIsConnected(): boolean {
    return this.isConnected
  }

  public getCompletedTranslations(): Map<string, TranslationResult> {
    return this.translations
  }
}

const wsClient = new TranslationWebSocket()
export default wsClient
