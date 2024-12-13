import { describe, test, expect } from 'vitest'
import { ModelArtifact } from './artifact'

describe('Model Artifact', () => {
  test('should create artifact with path', () => {
    const artifact1 = new ModelArtifact({
      name: 'test',
      path: 'Users\\jsmith\\Projects\\sqlmesh\\examples\\sushi',
    })

    expect(artifact1.path).toBeTruthy()
    expect(artifact1.path).toBe(
      'Users\\jsmith\\Projects\\sqlmesh\\examples\\sushi',
    )

    const artifact2 = new ModelArtifact({
      name: 'test',
      path: 'Users\\jsmith\\Projects\\sqlmesh\\examples\\sushi',
    })

    expect(artifact2.path).toBeTruthy()
    expect(artifact2.path).toBe(
      'Users\\jsmith\\Projects\\sqlmesh\\examples\\sushi',
    )
  })
})
